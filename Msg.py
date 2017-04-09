#!/usr/bin/env python3
#coding:utf-8

import time

class NewsItem(object):

    def __init__(self, title,desc,pic_url,url):
        self.title = title
        self.desc = desc
        self.pic_url = pic_url
        self.url = url

    def __str__(self):
        template = '''
        <item>
            <Title><![CDATA[%s]]></Title>
            <Description><![CDATA[%s]]></Description>
            <PicUrl><![CDATA[%s]]></PicUrl>
            <Url><![CDATA[%s]]></Url>
        </item>
        '''
        return template % (self.title,self.desc,self.pic_url,self.url)

class Msg(object):

    def __init__(self,toUserName,fromUserName,MsgType):
        self.toUserName = toUserName
        self.fromUserName = fromUserName
        self.MsgType = MsgType

    def reply_text(self,text):

        template = '''<xml>
            <ToUserName><![CDATA[%s]]></ToUserName>
            <FromUserName><![CDATA[%s]]></FromUserName>
            <CreateTime>%s</CreateTime>
            <MsgType><![CDATA[text]]></MsgType>
            <Content><![CDATA[%s]]></Content>
        </xml>'''

        return template % (self.fromUserName,self.toUserName,int(time.time()),text)

    def reply_sound(self,title,desc,music_url,hq_url):
        template = '''<xml>
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
        </xml>'''
        return template % (self.toUserName, self.fromUserName, int(time.time()), \
                           title, desc, music_url, hq_url)

    def reply_image(self,media_id):
        template = '''<xml>
            <ToUserName><![CDATA[%s]]></ToUserName>
            <FromUserName><![CDATA[%s]]></FromUserName>
            <CreateTime>%s</CreateTime>
            <MsgType><![CDATA[image]]></MsgType>
            <Image>
            <MediaId><![CDATA[%s]]></MediaId>
            </Image>    
        </xml>'''
        return template % (self.toUserName, self.fromUserName, int(time.time()), media_id)

    def resp_news(self,news_items):
        template = '''<xml>
            <ToUserName><![CDATA[%s]]></ToUserName>
            <FromUserName><![CDATA[%s]]></FromUserName>
            <CreateTime>%s</CreateTime>
            <MsgType><![CDATA[news]]></MsgType>
            <ArticleCount>%s</ArticleCount>
            <Articles>
              %s
            </Articles>
        </xml>'''
        return template % (self.toUserName, self.fromUserName, int(time.time()), len(news_items), (''.join(news_items)))

