# 学習済みモデルお試しbot

## 概要

学習済みモデルお試しbotは、Pythonで開発されたLINE BOTです。ユーザーが画像を送信すると、事前に学習済みのPytorchモデルを使用して画像分類を行い、その結果をユーザーに返信します。ユーザーはテキストメッセージでモデル名を指定することで、使用するモデルを切り替えることができます。

## 動作例

1. ユーザーがBOTにテキストメッセージを送信し、使用するモデル名を指定します（例: "resnet18"）。
2. ユーザーがBOTに画像を送信します。
3. BOTは指定されたモデルを使用して画像分類を行い、結果をユーザーに返信します。

## 設定方法

### 必要なもの

- Python 3.x
- LINE Developers アカウント
- Pythonライブラリ（torch、torchvision、flask、line-bot-sdk、pillow、numpy）
- imagenet_class_index.json（別途ダウンロードが必要）

### 手順

1. このリポジトリをクローンまたはダウンロードします。
2. プロジェクトのディレクトリに移動します。
3. 必要なPythonライブラリをインストールします。
pip install -r requirements.txt

4. imagenet_class_index.jsonをダウンロードし、プロジェクトのルートディレクトリに配置します。
- ダウンロードリンク: [imagenet_class_index.json](https://github.com/raghakot/keras-vis/blob/master/resources/imagenet_class_index.json)

5. LINE Developersコンソールで新しいBOTを作成し、チャネルアクセストークンとチャネルシークレットを取得します。

6. app.pyファイルを開き、チャネルアクセストークンとチャネルシークレットを設定します。
```python
line_bot_api = LineBotApi('YOUR_CHANNEL_ACCESS_TOKEN')
handler = WebhookHandler('YOUR_CHANNEL_SECRET')

7. app.pyファイルを開き、チャネルアクセストークンとチャネルシークレットを設定します。
python app.py

8. ngrokを使用してローカルサーバーを公開し、LINE DevelopersコンソールでWebhook URLを設定します。
9. LINEアプリでBOTを友達に追加し、画像を送信して動作を確認します。

注意: imagenet_class_index.jsonは別途ダウンロードが必要です。プロジェクトのルートディレクトリに配置してください。


このREADME.mdは、プロジェクトの概要、動作例、設定方法を説明しています。必要に応じて、内容を追加したり、プロジェクトの要件に合わせて修正したりしてください。
ライセンスについては、プロジェクトがオープンソースでない限り、必須ではありません。ただし、商用利用や再配布を制限したい場合は、適切なライセンスを選択し、READMEやLICENSEファイルに記載することをお勧めします。