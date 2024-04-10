from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageMessage
import torchvision.models as models
from torchvision import transforms
from PIL import Image
import torch
import json
import logging


app = Flask(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)

line_bot_api = LineBotApi('')
handler = WebhookHandler('')

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model_cache = {}

transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

def load_model(model_name):
    if model_name not in model_cache:
        try:
            model = getattr(models, model_name)(pretrained=True)
            model.to(device)
            model.eval()
            model_cache[model_name] = model
            logging.info(f"{model_name} model loaded and cached.")
        except AttributeError:
            logging.warning(f"{model_name} model not found.")
            return None
    else:
        logging.info(f"{model_name} model loaded from cache.")
    return model_cache[model_name]

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    logging.info(f"Request body: {body}")
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text.strip().lower()
    
    if text in dir(models):
        model = load_model(text)
        if model is not None:
            reply_text = f"{text}モデルが読み込まれました。画像を送信してください。"
        else:
            reply_text = f"{text}モデルは存在しません。別のモデル名を入力してください。"
    else:
        reply_text = f"{text}モデルは存在しません。別のモデル名を入力してください。"
        
    logging.info(f"Received message: {event.message.text}, Reply: {reply_text}")
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text))

@handler.add(MessageEvent, message=ImageMessage)
def handle_image(event):
    if not model_cache:
        reply_text = "モデルが読み込まれていません。先にモデル名を入力してください。"
    else:
        logging.info(f"Received image")
        message_content = line_bot_api.get_message_content(event.message.id)
        with open('temp_image.jpg', 'wb') as f:
            f.write(message_content.content)
        logging.info(f"Image saved as temp_image.jpg")
        
        try:
            img = Image.open('temp_image.jpg')
            logging.info(f"Image loaded")
            img = transform(img).unsqueeze(0)
            img = img.to(device)
            logging.info(f"Image preprocessed")
            
            model_name, model = next(iter(model_cache.items()))
            
            with torch.no_grad():
                outputs = model(img)
            logging.info(f"Image classification completed")
            
            _, preds = torch.max(outputs, 1)
            
            with open('imagenet_class_index.json') as f:
                class_idx = json.load(f)
            
            result = [class_idx[str(k)][1] for k in preds.tolist()]
            reply_text = f"分類結果: {result[0]} ({model_name}モデルによる予測)"
            logging.info(f"Classification result: {reply_text}")
        except Exception as e:
            logging.error(f"Error occurred: {str(e)}")
            reply_text = "エラーが発生しました。画像の処理に失敗しました。"
    
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text))
    logging.info(f"Reply message sent")

if __name__ == "__main__":
    app.run()
