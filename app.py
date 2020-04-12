#!/usr/bin/python3
from flask import Flask, request, abort
from linebot.exceptions import InvalidSignatureError
import bot

app = Flask(__name__)
app.debug = True

@app.route("/line-webhook", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        bot.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'