from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from firebase_utils import store_message, summarize_unread_messages
from config import LINE_CHANNEL_ACCESS_TOKEN, LINE_CHANNEL_SECRET

app = Flask(__name__)

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == "!summary":
        group_id = event.source.group_id
        summary = summarize_unread_messages(group_id)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=summary)
        )
    else:
        store_message(event.source.group_id, event.source.user_id, event.message.text)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    
    return 'OK'

if __name__ == "__main__":
    app.run()