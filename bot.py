from linebot import (
    LineBotApi, WebhookHandler
)

from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

from utils import get_source_id
from config import config
from message import RelayMessageSender

line_bot_api = LineBotApi(config.get('access_token'))
handler = WebhookHandler(config.get('secret'))

def handle(body, signature):
    return handler.handle(body, signature)

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    sender = RelayMessageSender(timeout=int(config.get('chat_timeout')),
                                email_domain=config.get('email_domain'),
                                to_email=config.get('recipient_email'),
                                to_name=config.get('recipient_name'))

    message = event.message.text
    msg_lower = message.lower()

    if (msg_lower == "/forgetme"):
        pass
    elif (message == '/uid'):
        source_id = get_source_id(event)
        response = TextSendMessage(text=source_id)
        try:
            line_bot_api.reply_message(event.reply_token, response)
        except Exception as e:
            print(e)
    else:
        user_id = get_source_id(event)
        sender.record_message(user_id, message)
