from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render

# ! /usr/bin/env python
# -*- coding: utf-8 -*-
# Date: 2017/9/25


import re
import urllib.request

import http.cookiejar
from bs4 import BeautifulSoup

from collections import deque

from clubApp.models import Club, League

# Create your views here.
from playerApp.models import Player, PlayPosition


def get_other(request):
    League.objects.create(l_name='德甲')
    League.objects.create(l_name='法甲')
    League.objects.create(l_name='西甲')
    League.objects.create(l_name='意甲')
    League.objects.create(l_name='英超')

    PlayPosition.objects.create(position='其他')
    PlayPosition.objects.create(position='前锋')
    PlayPosition.objects.create(position='中场')
    PlayPosition.objects.create(position='后卫')
    PlayPosition.objects.create(position='守门员')
    return HttpResponse('...')


def get_player(request):
    queue = deque()
    visited = set()

    def makeMyOpener(head={
        'Connection': 'Keep-Alive',
        'Accept': 'text/html, application/xhtml+xml, */*',
        'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
    }):
        cj = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        header = []
        for key, value in head.items():
            elem = (key, value)
            header.append(elem)
        opener.addheaders = header
        return opener

    # f_url = 'http://qiudui.caipiao.163.com/9/0000/884/qdzr.html'  # 德甲  入口页面, 可以换成别的
    # f_url = 'http://qiudui.caipiao.163.com/16/14060/884/qdzr.html'  # 法甲 入口页面, 可以换成别的
    # f_url = 'http://qiudui.caipiao.163.com/7/0000/884/qdzr.html'  # 西甲 入口页面, 可以换成别的
    # f_url = 'http://qiudui.caipiao.163.com/13/0000/884/qdzr.html'  # 意甲 入口页面, 可以换成别的
    # f_url = 'http://qiudui.caipiao.163.com/8/0000/884/qdzr.html'  # 英超 入口页面, 可以换成别的

    f_url = ['http://qiudui.caipiao.163.com/9/0000/884/qdzr.html',
             'http://qiudui.caipiao.163.com/16/14060/884/qdzr.html',
             'http://qiudui.caipiao.163.com/7/0000/884/qdzr.html',
             'http://qiudui.caipiao.163.com/13/0000/884/qdzr.html',
             'http://qiudui.caipiao.163.com/8/0000/884/qdzr.html',
             ]
    index_num = 0
    for url in f_url:
        index_num += 1
        queue.append(url)
        oper = makeMyOpener()
        m_request = oper.open(url, timeout=2)
        # 获取返回结果
        m_data1 = m_request.read().decode('utf-8')

        soup = BeautifulSoup(m_data1, 'html.parser')
        tr = soup.select('.teameInfo ul li a')

        for u in tr:
            uu = u.get('href')
            uu = uu.replace('scpl', 'qdzr')
            if uu in f_url:
                continue
            # print(uu)
            queue.append(uu)

        while queue:
            url = queue.popleft()  # 队首元素出队
            print(url)
            if url in visited:
                continue
            visited |= {url}
            m_request = oper.open(url, timeout=2)

            m_data1 = m_request.read().decode('utf-8')

            soup = BeautifulSoup(m_data1, 'html.parser')
            club_name = soup.select('.teamDetail .title')[0].find('strong').get_text()
            club = Club.objects.create(c_name=club_name, l_name_id=index_num)
            c_id = club.id
            # c_id = index_num
            tr = soup.select('.lineupBox ul')
            p_num = 1
            for line in tr:
                p_num += 1
                name_em = line.find_all('li')
                for name in name_em:
                    play_name = name.find('em').get_text()
                    # print(play_name)
                    Player.objects.create(name=play_name, c_name_id=c_id, position_id=p_num)
    return HttpResponse('...')


def get_play(request):
    queue = deque()
    visited = set()

    def makeMyOpener(head={
        'Connection': 'Keep-Alive',
        'Accept': 'text/html, application/xhtml+xml, */*',
        'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
    }):
        cj = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        header = []
        for key, value in head.items():
            elem = (key, value)
            header.append(elem)
        opener.addheaders = header
        return opener

    # f_url = 'http://qiudui.caipiao.163.com/9/0000/884/qdzr.html'  # 德甲  入口页面, 可以换成别的
    # f_url = 'http://qiudui.caipiao.163.com/16/14060/884/qdzr.html'  # 法甲 入口页面, 可以换成别的
    # f_url = 'http://qiudui.caipiao.163.com/7/0000/884/qdzr.html'  # 西甲 入口页面, 可以换成别的
    # f_url = 'http://qiudui.caipiao.163.com/13/0000/884/qdzr.html'  # 意甲 入口页面, 可以换成别的
    # f_url = 'http://qiudui.caipiao.163.com/8/0000/884/qdzr.html'  # 英超 入口页面, 可以换成别的

    f_url = [
        'http://saishi.caipiao.163.com/9/14007.html?weekId=1&groupId=&roundId=41485&indexType=0&guestTeamId=',
        'http://saishi.caipiao.163.com/16/14060.html?weekId=1&groupId=&roundId=41646&indexType=0&guestTeamId=',
        'http://saishi.caipiao.163.com/7/14018.html?weekId=1&groupId=&roundId=41509&indexType=0&guestTeamId=',
        'http://saishi.caipiao.163.com/13/14181.html?weekId=1&groupId=&roundId=42011&indexType=0&guestTeamId=',
        'http://saishi.caipiao.163.com/8/14029.html?weekId=1&groupId=&roundId=41547&indexType=0&guestTeamId=',
             ]
    index_num = 0
    for url in f_url:
        index_num += 1
        oper = makeMyOpener()
        m_request = oper.open(url, timeout=2)
        # 获取返回结果
        m_data1 = m_request.read().decode('utf-8')

        soup = BeautifulSoup(m_data1, 'html.parser')
        tr = soup.select('.turnTime  dl dd a')

        for u in tr:
            uu = u.get('href')
            uu = 'http://saishi.caipiao.163.com' + uu
            # print(uu)
            queue.append(uu)

        while queue:
            url = queue.popleft()  # 队首元素出队
            # print(url)
            if url in visited:
                continue
            visited |= {url}
            m_request = oper.open(url, timeout=2)

            m_data1 = m_request.read().decode('utf-8')

            soup = BeautifulSoup(m_data1, 'html.parser')
            play_list = soup.select('.listWrap table tr')[2:]
            for play in play_list:
                info = play.find_all('td')
                # print(info)
                bifen = info[2].get_text()
                if bifen == '未开赛':
                    queue.clear()
                    break
                bifen = bifen.split(':')
                z_goal = int(bifen[0])
                k_goal = int(bifen[1])
                time = info[0].get_text()
                start_date = datetime.strptime(time, "%Y-%m-%d %h:%m")
                z_name = info[1].find('a').get('title')
                k_name = info[3].find('a').get('title')
                z_name = Club.objects.filter(c_name=z_name).first().id
                k_name = Club.objects.filter(c_name=k_name).first().id
                if z_goal > k_goal:
                    p_result = 1
                elif z_goal == k_goal:
                    p_result = 0
                else:
                    p_result = 2
                z_peilv = info[5].get_text()
                p_peilv = info[6].get_text()
                k_peilv = info[7].get_text()
                print(time, z_name, bifen, k_name, z_peilv, p_peilv, k_peilv)

    return HttpResponse('...')

