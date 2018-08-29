# encoding=utf-8
from flask import Flask, request, abort, jsonify

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

import requests
import pymysql
import requests
import jieba
from controller import blueprint
from model import DBSession
from model.userInfo import userinfo

jieba.load_userdict("sc-dictionary/main.txt")

db = DBSession()

line_bot_api = LineBotApi('Rh6P7TDiSyGq3GhWWjg+KlHuN5GzsIsYKDX9qQkzdcAi0TbMKXITpoeDk8Ra0oPIx0kg21gconwSHPqMJpa/q6s2DQAMHWZwawJ3nbd0lL3SCWk3xWJs/tAHOlDjgL1GB1ZT6EPpcFHDlmNGjvYXSwdB04t89/1O/w1cDnyilFU=')

handler = WebhookHandler('5e5b5da4cd536c401c179da733566473')

def connectToSql():
    sql = pymysql.connect("localhost","ubuntu","hellohello","chatbot")
    return sql

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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == 'Hello':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='Hello'))

    elif event.message.text == 'How are you':
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='Good.')
        )

    elif event.message.text == "godfrey8581":
        # sql= connectToSql()
        # cur = sql.cursor()
        # cur.execute("SELECT user_id FROM userinfo")
        # user_ids = cur.fetchall()
        user_ids = db.query(USERINFO.user_id).all()

        for user_id in user_ids:
            line_bot_api.push_message(user_id[0], TextSendMessage(text="WWWW"))

        sql.commit()
        sql.close()

    else:
        data = {'question':event.message.text}
        r = requests.post('http://0.0.0.0:8000/chatbot/questionAnswer',json=data)
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r.json()['answer'])
        )


# 告知handler，如果收到FollowEvent，則做下面的方法處理
@handler.add(FollowEvent)
def reply_text_and_get_user_profile(event):

    # 取出消息內User的資料
    user_profile = line_bot_api.get_profile(event.source.user_id)

     # 將用戶資訊存在SQL內

    sql = connectToSql()
    cur = sql.cursor()
    cur.execute("SELECT user_id FROM userinfo WHERE user_id = '{}'".format(user_profile.user_id))
    userIds = cur.fetchall()

    print(userIds)

    if userIds == ():
        cur.execute("INSERT INTO userinfo (displayname, picture_url, status_message, user_id) VALUES ('{}','{}','{}','{}')".format(user_profile.display_name, user_profile.picture_url, user_profile.status_message, user_profile.user_id))
        sql.commit()
        sql.close()

    line_bot_api.push_message(user_profile.user_id,TextSendMessage(text='Hello'))

@blueprint.route("/controlNLP", methods=['POST'])
def controlNLP():
    intentsOpen = ["開","打開","開啟"]
    intentsClose = ["關","關掉","關閉"]
    intents_1 = ["開燈","關燈","燈","電燈","LED","冷氣","空氣清淨機","電視","門"]
    userIntent = request.get_json()
    # print(userIntent['userIntent'])
    userIntent = jieba.cut_for_search(userIntent["userIntent"])

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
