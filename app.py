import os
import dotenv
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import facebook_crawler

app = Flask(__name__)
handler = WebhookHandler('1f444a9a19a4d517cbe5689b7c89789b')


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK', 200


class LineBot:
    def __init__(self, ID, event, msg) -> None:
        self.line_bot_api = LineBotApi(os.getenv("LINE_BOT_API_TOKEN"))
        self.event = event
        self.ID = ID
        self.msg = msg

    def reply_msg(self, msg) -> None:
        self.line_bot_api.reply_message(
            self.event.reply_token, TextSendMessage(msg))

    def push_msg(self, msg) -> None:
        self.line_bot_api.reply_message(
            self.event.reply_token, TextSendMessage(msg))


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    dotenv.load_dotenv()
    access_token = os.getenv('ACCESS_TOKEN')
    video_ids = {
        '1032184421373970': 'FRIGPATHY',
        '896707631835497': 'GaiaBit毛焦點靚青春',
        '884820739683019': 'JLL',
        '357195453630410': 'Vitawear 戴命醫電',
        '994616074971005': '捷足AgileFoot',
        '751091986837645': '運動揪揪',
        '909824847528125': '嘿疲YOLO乳'
    }
    Linebot = LineBot(event.source.user_id, event, event.message.text)
    if Linebot.msg == "若水":
        likes_counts = facebook_crawler.fetch_facebook_likes(
            access_token, video_ids)
        Linebot.msg = facebook_crawler.display_sorted_likes(likes_counts)
        print(Linebot.msg)
        Linebot.reply_msg(Linebot.msg)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
