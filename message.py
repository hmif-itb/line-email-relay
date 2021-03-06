import time
from threading import Timer
import random
from db import ChatBubble
from utils import generate_random_name
from email_sender import send_email
from db import Participant
from linebot.models import TextSendMessage

timer_map = dict()

class RelayMessageHandler:
    message_timeout = 60 #seconds

    def __init__(self, line_bot_api, email_domain, to_email, to_name, timeout=60, enquiry_received_reply=None):
        self.line_bot_api = line_bot_api
        self.message_timeout = timeout
        self.email_domain = email_domain
        self.to_email = to_email
        self.to_name = to_name
        self.enquiry_received_reply = enquiry_received_reply

    def record_message(self, user_id, message):
        chat_bubble = ChatBubble(message=message, user_id=user_id, timestamp=int(time.time()))
        chat_bubble.save()
        self._schedule_message(self.message_timeout, user_id)

    def _relay_messages_to_email(self, user_id):
        chat_bubbles = ChatBubble.select().where(ChatBubble.user_id == user_id).order_by(ChatBubble.timestamp.asc())

        messages = []
        for chat_bubble in chat_bubbles:
            messages.append("> " + chat_bubble.message)

        ChatBubble.delete().where(ChatBubble.user_id == user_id).execute()

        try:
            participant = Participant.select().where(Participant.line_mid == user_id).get()
            email_id = participant.email_id
            name = participant.name
        except:
            email_id = '%30x' % random.randrange(16 ** 30)
            name = generate_random_name()
            participant = Participant(line_mid=user_id, email_id=email_id, name=name)
            participant.save()

        recipient = f"{email_id}@{self.email_domain}"
        body = "\n".join(messages)

        subject = f"Incoming Message from {name}"
        send_email(recipient, name, self.to_email, self.to_name, subject, body)

        if (self.enquiry_received_reply):
            self.line_bot_api.push_message(user_id, TextSendMessage(text=self.enquiry_received_reply))

    def _get_time_to_send(self, user_id):
        chat_bubble = ChatBubble.select().where(ChatBubble.user_id == user_id).order_by(ChatBubble.timestamp.desc()).get()
        time_since_last_message = int(chat_bubble.timestamp)
        time_message_should_be_sent = time_since_last_message + self.message_timeout
        time_to_send = time_message_should_be_sent - int(time.time())

        return time_to_send

    def _perform_schedule_check(self, user_id):
        time_to_send = self._get_time_to_send(user_id)

        if (time_to_send <= 0):
            self._relay_messages_to_email(user_id)
        else:
            self._schedule_message(time_to_send, user_id)

    def _schedule_message(self, seconds, user_id):
        if (user_id in timer_map):
            timer = timer_map[user_id]
            timer.cancel()

        timer = Timer(seconds, self._perform_schedule_check, list([user_id]))
        timer.start()
        timer_map[user_id] = timer
