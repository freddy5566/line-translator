from flask import Flask, request, abort
from translator import Translator
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import os

app = Flask(__name__)
translator = Translator()

line_bot_api = LineBotApi(os.environ['YOUR_CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['YOUR_CHANNEL_SECRET'])


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


def handle_translation(message):
    translator = Translator()
    translator.detect_language(message)
    result = None
    try:
        result = translator.translate_text_with_model(
            translator.target_language, message)
    except:
        result = 'Sorry cannnot translate your message'
    return result


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    translated_result = handle_translation(event.message.text)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=translated_result))


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
