# encoding=utf-8
from flask import Flask, request, abort, jsonify

from controller import blueprint
'''
Linebot is the offical sdk api of line
The all detail of the linebot sdk can visit this github repository:
https://github.com/line/line-bot-sdk-python
'''
from linebot import (
    LineBotApi, WebhookHandler
)

from linebot.exceptions import (
    InvalidSignatureError
)

from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage
)

from linebot.models.events import (
    FollowEvent
)

from linebot.models.events import (
    UnfollowEvent
)

import requests
import pymysql
import requests
import jieba
from model import DBSession
from model.userInfo import userinfo
from time import gmtime, strftime

# The traditional chinese dictionary for cut word
# jieba.load_userdict("sc-dictionary/main.txt")
app = Flask(__name__)

'''
Add your token and secret key in t
line_bot_api = LineBotApi('YOUR_CHANNEL_ACCESS_TOKEN')
handler = WebhookHandler('YOUR_CHANNEL_SECRET')
'''
line_bot_api = LineBotApi('Rh6P7TDiSyGq3GhWWjg+KlHuN5GzsIsYKDX9qQkzdcAi0TbMKXITpoeDk8Ra0oPIx0kg21gconwSHPqMJpa/q6s2DQAMHWZwawJ3nbd0lL3SCWk3xWJs/tAHOlDjgL1GB1ZT6EPpcFHDlmNGjvYXSwdB04t89/1O/w1cDnyilFU=')

handler = WebhookHandler('5e5b5da4cd536c401c179da733566473')

# Connect to line server
@blueprint.route("/callback", methods=['POST'])
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
            abort(400)

        return 'OK'

# This route is for IoT chatbot
@blueprint.route("/controlNLP", methods=['POST'])
def controlNLP():
    intentsOpen = ["開","打開","開啟"]
    intentsClose = ["關","關掉","關閉"]
    intents_1 = ["開燈","關燈","燈","電燈","LED","冷氣","空氣清淨機","電視","門"]
    userIntent = request.get_json()
    userIntentAfterCut = jieba.cut_for_search(userIntent["userIntent"])

    intent = ""

    for word in userIntentAfterCut:
        print(word)
        if word in intentsOpen:
            intent += "開"
        elif word in intentsClose:
            intent += "關"
        elif word in intents_1:
            intent += word
    if intent:
        return userIntent['userIntent']
    else:
        return intent
'''
When server get the message from line, the server will return the
message recording to the user input.
event.message.text is the user input

Reply message to user
ine_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='some text'))

'''
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_profile = line_bot_api.get_profile(event.source.user_id)

    if event.message.text == 'Hello':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='Hello ! ' + user_profile.display_name))

    elif event.message.text == 'How are you':
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='Good.')
        )

    elif event.message.text == "godfrey8581":
        db = DBSession()
        user_ids = db.query(userinfo.user_id).all()

        if user_ids != []:
            for user_id in user_ids:
                line_bot_api.push_message(user_id[0], TextSendMessage(text="WWWW"))

        db.commit()
        db.close()

    # else:
        # data = {'question':event.message.text}
        # r = requests.post('http://0.0.0.0:8000/chatbot/questionAnswer',json=data)
        # line_bot_api.reply_message(
        # event.reply_token,
        # TextSendMessage(text=r.json()['answer'])
        # )


# 告知handler，如果收到FollowEvent，則做下面的方法處理
@handler.add(FollowEvent)
def reply_text_and_get_user_profile(event):

    # 取出消息內User的資料
    user_profile = line_bot_api.get_profile(event.source.user_id)
    date = strftime("%Y-%m-%d", gmtime())

    db = DBSession()
    userIds = db.query(userinfo.user_id).all()

    if userIds == []:
        db = DBSession()
        user = userinfo(date ,user_profile.display_name, user_profile.picture_url,user_profile.status_message, user_profile.user_id)
        db.add(user)
    db.commit()
    db.close()

    line_bot_api.push_message(user_profile.user_id,TextSendMessage(text='Hello'))

@handler.add(UnfollowEvent)
def user_unfollow_delete_userInfo(event):
    connection = pymysql.connect(host='localhost',
                    user='root',
                    password='hellohello',
                    db='chatbot',
                    charset='utf8'
                    )
    cursor = connection.cursor()
    cursor.execute("DELETE FROM userinfo WHERE user_id='{}'".format(event.source.user_id))
    connection.commit()
    connection.close()

    intent = ""

    for word in userIntent:
        print(word)
        if word in intentsOpen:
            intent += "開"
        elif word in intentsClose:
            intent += "關"
        elif word in intents_1:
            intent += word

    return intent
