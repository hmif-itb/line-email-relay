from message import RelayMessageSender
import time

sender = RelayMessageSender(timeout=10, email_domain="akscrbot.hmif.tech")

sender.record_message("u2", "Hello!")
time.sleep(5)
sender.record_message("u2", "How are you?")
time.sleep(1)
sender.record_message("u3", "I hope you're okay")
time.sleep(2)
sender.record_message("u3", "Thanks!")