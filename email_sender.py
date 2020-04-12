from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from config import config
password = config.get('smtp_password')
username = config.get('smtp_user')
smtphost = f"{config.get('smtp_host')}:{config.get('smtp_port')}"

def send_email(from_email, from_name, to_email, to_name, message):
    print(f"Sending email from {from_name} <{from_email}> to {to_name} <{to_email}>")
    print(message)

    server = smtplib.SMTP(smtphost)
    server.starttls()
    server.login(username, password)

    msg = MIMEMultipart()
    msg['From'] = f"{from_name} <{from_email}>"
    msg['To'] = f"{to_name} <{to_email}>"
    msg['Subject'] = f"Incoming Message from Anonymous {from_name}"

    msg.attach(MIMEText(message, 'plain'))

    server.sendmail(msg['From'], msg['To'], msg.as_string())

    server.quit()