from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from app.firebase import get_new_messages
from app.config import Config

line_bot_api = LineBotApi(Config.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(Config.LINE_CHANNEL_SECRET)

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == "新訊息摘要":
        new_messages = get_new_messages(event.source.group_id)
        summary = "\n".join(new_messages)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=summary)
        )

def handle_line_event(body, signature):
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        raise ValueError("Invalid signature. Check your channel access token/channel secret.")
