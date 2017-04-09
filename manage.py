#!/usr/bin/env python3
# coding:utf-8

import time
from flask import Flask, request, make_response
import hashlib
from bs4 import BeautifulSoup
import json
import requests
import re
from Msg import Msg

app = Flask(__name__)

APPID = 'wxcdf195293151f105'
APPSECRET = 'db2fead72717453b193333703d617011'

# EventType = {
#     "subscribe": onSubscribe,
#     "unsubscribe": onUnsubscribe,
#     "scan": onScan,
#     "location": onEventLocation,
#     "click": onClick,
#     "view": onView
# }

def get_access_token(appid,appsecret):
    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={0}&secret={1}'.format(appid,appsecret)
    resp = requests.get(url).text
    return json.loads(resp).get('access_token')

def delete_menus(access_token):
    url = 'https://api.weixin.qq.com/cgi-bin/menu/delete?access_token=%s' % access_token
    resp = requests.get(url)
    return resp.text

def create_menus(access_token):
    url = 'https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s' % access_token
    data = {
        "button": [
            {
                "type": "click",
                "name": "今日电台",
                "key": "TODAY_MUSIC"
            },
            {
                "name": "菜单",
                "sub_button": [
                    {
                        "type": "view",
                        "name": "搜索",
                        "url": "http://www.baidu.com/"
                    },
                    {
                        "type": "click",
                        "name": "赞一下我们",
                        "key": "V1001_GOOD"
                    }
                ]
            }
        ]
    }
    resp = requests.post(url,data=data)
    return resp.text

@app.route('/wechat', methods=['GET', 'POST'])
def wechat():
    if request.method == 'GET':
        token = 'wechat'
        query = request.args
        signature = query.get('signature', '')
        timestamp = query.get('timestamp', '')
        nonce = query.get('nonce', '')
        echostr = query.get('echostr', '')
        s = [timestamp, nonce, token]
        s.sort()
        s = ''.join(s).encode('utf-8')
        if (hashlib.sha1(s).hexdigest() == signature):
            return make_response(echostr)
        else:
            print(' 该请求不是来自于微信...')
    # else:
    #     xml_recv = ET.fromstring(request.data)
    #     ToUserName = xml_recv.find("ToUserName").text
    #     FromUserName = xml_recv.find("FromUserName").text
    #     Content = xml_recv.find("Content").text
    #     reply = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%s]]></Content><FuncFlag>0</FuncFlag></xml>"
    #     response = make_response(reply % (FromUserName, ToUserName,
    #                                       str(int(time.time())), Content))
    #     response.content_type = 'application/xml'
    #     return response

    if request.method == 'POST':
        soup = BeautifulSoup(request.data, 'xml')
        toUserName = soup.find('ToUserName').text
        fromUserName = soup.find('FromUserName').text
        msgType = soup.find('MsgType').text
        msg = Msg(toUserName, fromUserName, msgType)

        if msgType == 'event':
            content = soup.find('Event').text
            if content == 'subscribe':
                text = '欢迎关注公众号...'
                response = make_response(msg.reply_text(text))
                return response
            elif content == 'CLICK':
                key_value = soup.find('EventKey').get_text()
                response = make_response(msg.reply_text(key_value))
                return response


        if msgType == 'text':

            content = soup.find('Content').get_text()
            key = '64fe923bce7b4eb8b0d169386fa745fe'
            api = 'http://www.tuling123.com/openapi/api?key=' + key + '&info='
            url = api + content
            content = json.loads(requests.get(url).text)['text']
            response = make_response(msg.reply_text(content))

            return response

            # if content == 'FM' or content == 'fm' or content == u'电台':
            #     url = 'http://m.xinli001.com/fm/'
            #     data = requests.get(url).text
            #     soup2 = BeautifulSoup(data, 'lxml')
            #     title = soup2.find('div', attrs={'class': 'infor'}).find('p').text
            #     pa3 = re.compile(r'var broadcast_url = "(.*?)", broadcastListUrl = "/fm/items/', re.S)
            #     ts3 = re.findall(pa3, data)
            #     musicTitle = title
            #     musicDes = ''
            #     musicURL = ts3[0]
            #     HQURL = ts3[0]
            #     response = make_response(reply_sound % (
            #     fromUserName, toUserName, str(int(time.time())), musicTitle, musicDes, musicURL, HQURL))
            #     response.content_type = 'application/xml'
            #     return response
            # if content == u'中秋':
            #     title1 = 'happy autumn!'
            #     description1 = 'do not say anything'
            #     xc = 'http://viewer.maka.im/k/J64391B8'
            #     pic = 'http://pic33.nipic.com/20130923/11927319_180343313383_2.jpg'
            #     response = make_response(
            #         reply_pic % (fromUserName, toUserName, str(int(time.time())), title1, description1, pic, xc))
            #     response.content_type = 'application/xml'
            #     return response
                # return render_template('text.xml',fromUserName=fromUserName,toUserName=toUserName,createTime=createTime,content=content)


if __name__ == '__main__':
    access_token = get_access_token()
    delete_menus(access_token)
    # create_menus(access_token)
    app.run()
