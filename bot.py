from linebot import (
    LineBotApi, WebhookHandler
)

from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

from utils import get_source_id
from config import config
from message import RelayMessageHandler
from email_reply_parser import EmailReplyParser
from db import Participant

line_bot_api = LineBotApi(config.get('access_token'))
handler = WebhookHandler(config.get('secret'))

def handle(body, signature):
    return handler.handle(body, signature)

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    sender = RelayMessageHandler(line_bot_api=line_bot_api,
                                 timeout=int(config.get('chat_timeout')),
                                 email_domain=config.get('email_domain'),
                                 to_email=config.get('recipient_email'),
                                 to_name=config.get('recipient_name'),
                                 enquiry_received_reply=config.get('enquiry_received_reply'))

    message = event.message.text
    msg_lower = message.lower()

    if (msg_lower == "/forgetme"):
        source_id = get_source_id(event)
        Participant.delete().where(Participant.line_mid == source_id).execute()
        response = TextSendMessage(text="Identitas samaran kamu sudah diganti.")
        line_bot_api.reply_message(event.reply_token, response)

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


def relay_from_email(to_email, text_message):
    email_id = to_email.split('@')[0]
    text = EmailReplyParser.parse_reply(text_message)

    try:
        participant = Participant.select().where(Participant.email_id == email_id).get()
        line_mid = participant.line_mid
        line_bot_api.push_message(line_mid, TextSendMessage(text=text))
    except:
       pass