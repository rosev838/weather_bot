#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import urllib.request, urllib.error
import json
from slackbot.bot import resond_to     # @botname: で反応するデコーダ
from slackbot.bot import listen_to      # チャネル内発言で反応するデコーダ
from slackbot.bot import default_reply  # 該当する応答がない場合に反応するデコーダ

def open_id():
    ld = open("./id_list.txt")
    lines = ld.readlines()
    ld.close()
    return lines

def find_cityname(citycode, lines):
    for line in lines:
        if line.find(citycode) >= 0:
            #print line[:-1]
            citylist = line[:-1].split(" ")
            cityname = citylist[0].split("\"")
            #print cityname[1]
            return cityname

def find_citycode(cityname, lines):
    for line in lines:
        if line.find(cityname) >= 0:
            #print line[:-1]
            citylist = line[:-1].split(" ")
            citycode = citylist[1].split("\"")
            #print cityname[1]
            return citycode

def print_weather(res, cityname):
    print(u'今日から3日間の' + cityname[1] + 'の天気')
    for forecast in res['forecasts']:
        print('**************************')
        print(forecast['dateLabel']+'('+forecast['date']+')').encode('utf-8')
        print(forecast['telop']).encode('utf-8')
    print('**************************')

def printbot_weather(res, cityname, message):
    msg0 = '今日から3日間の' + cityname[1] + 'の天気'
    message.send(msg0)
    msg1 = '**************************'
    for forecast in res['forecasts']:
        msg2 = (forecast['dateLabel']+'('+forecast['date']+')').encode('utf-8')
        msg3 = (forecast['telop']).encode('utf-8')
        message.send(msg1)
        message.send(msg2)
        message.send(msg3)
    message.send(msg1)

def weather_reply(message):
    citycode = '130010' # デフォルトエリア : 東京
    
    res = urllib.request.urlopen(url='http://weather.livedoor.com/forecast/webservice/json/v1?city=%s'%citycode).read()
    
    # 読み込んだJSONデータを辞書型に変換
    res = json.loads(res)
    cityname = find_cityname(citycode, open_id())
    #print_weather(res, cityname)
    printbot_weather(res, cityname, message)


# bot宛のメッセージ
@resond_to(r'天気')
def mention_func(message):
    weather_reply(message)

# チャンネル内のbot宛以外の投稿
@listen_to(r'天気')
def listen_func(message):
    weather_reply(message)