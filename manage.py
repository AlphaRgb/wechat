#!/usr/bin/env python3
# coding:utf-8

import time
from flask import Flask, request, make_response
import hashlib
from bs4 import BeautifulSoup
import json
import requests
import re

app = Flask(__name__)


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
        createTime = str(int(time.time()))
        msgType = soup.find('MsgType').text

        # 文本消息模板
        reply_text = u'''
        <xml>
            <ToUserName><![CDATA[%s]]></ToUserName>
            <FromUserName><![CDATA[%s]]></FromUserName>
            <CreateTime>%s</CreateTime>
            <MsgType><![CDATA[%s]]></MsgType>
            <Content><![CDATA[%s]]></Content>
        </xml>    
        '''

        # 音频消息模板
        reply_sound = u'''
        <xml>
            <ToUserName><![CDATA[%s]]></ToUserName>
            <FromUserName><![CDATA[%s]]></FromUserName>
            <CreateTime>%s</CreateTime>
            <MsgType><![CDATA[music]]></MsgType>
            <Music>
            <Title><![CDATA[%s]]></Title>
            <Description><![CDATA[%s]]></Description>
            <MusicUrl><![CDATA[%s]]></MusicUrl>
            <HQMusicUrl><![CDATA[%s]]></HQMusicUrl>
            </Music>
        </xml>
        '''

        # 图片消息模板
        reply_pic = u'''
        <xml>
            <ToUserName><![CDATA[%s]]></ToUserName>
            <FromUserName><![CDATA[%s]]></FromUserName>
            <CreateTime>%s</CreateTime>
            <MsgType><![CDATA[news]]></MsgType>
            <ArticleCount>1</ArticleCount>
            <Articles>
            <item>
            <Title><![CDATA[%s]]></Title>
            <Description><![CDATA[%s]]></Description>
            <PicUrl><![CDATA[%s]]></PicUrl>
            <Url><![CDATA[%s]]></Url>
            </item>
            </Articles>
        </xml>'''

        if msgType == 'event':
            content = soup.find('Event').text
            if content == 'subscribe':
                text = u'hello!'
                response = make_response(reply_text % (fromUserName, toUserName, str(int(time.time())), msgType, text))
                response.content_type = 'application/xml'
                return response
            elif content == 'unsubscribe':
                print(1)
                return None

        if msgType == 'text':
            content = soup.find('Content').text
            if content == 'FM' or content == 'fm' or content == u'电台':
                url = 'http://m.xinli001.com/fm/'
                data = requests.get(url).text
                soup2 = BeautifulSoup(data, 'lxml')
                title = soup2.find('div', attrs={'class': 'infor'}).find('p').text
                pa3 = re.compile(r'var broadcast_url = "(.*?)", broadcastListUrl = "/fm/items/', re.S)
                ts3 = re.findall(pa3, data)
                musicTitle = title
                musicDes = ''
                musicURL = ts3[0]
                HQURL = ts3[0]
                response = make_response(reply_sound % (
                fromUserName, toUserName, str(int(time.time())), musicTitle, musicDes, musicURL, HQURL))
                response.content_type = 'application/xml'
                return response
            if content == u'中秋':
                title1 = 'happy autumn!'
                description1 = 'do not say anything'
                xc = 'http://viewer.maka.im/k/J64391B8'
                pic = 'http://pic33.nipic.com/20130923/11927319_180343313383_2.jpg'
                response = make_response(
                    reply_pic % (fromUserName, toUserName, str(int(time.time())), title1, description1, pic, xc))
                response.content_type = 'application/xml'
                return response
                # return render_template('text.xml',fromUserName=fromUserName,toUserName=toUserName,createTime=createTime,content=content)


if __name__ == '__main__':
    app.run()
