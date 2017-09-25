#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Date: 2017/9/25


import re
import urllib.request

import http.cookiejar
from bs4 import BeautifulSoup

from collections import deque

from clubApp.models import Club

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


f_url = 'http://qiudui.caipiao.163.com/7/14018/2016/qdzr.html'  # 入口页面, 可以换成别的
queue.append(f_url)
oper = makeMyOpener()
m_request = oper.open(f_url, timeout=2)
# 获取返回结果
m_data1 = m_request.read().decode('utf-8')

soup = BeautifulSoup(m_data1, 'html.parser')
tr = soup.select('.teameInfo ul li a')

for u in tr:
    uu = u.get('href')
    uu = uu.replace('scpl', 'qdzr')
    # print(uu)
    queue.append(uu)

cnt = 0

while queue:
    url = queue.popleft()  # 队首元素出队
    print(url)
    if url in visited:
        continue
    visited |= {url}
    m_request = oper.open(url, timeout=2)

    m_data1 = m_request.read().decode('utf-8')

    soup = BeautifulSoup(m_data1, 'html.parser')
    club_name = soup.select('.teamDetail .title strong').get_text()
    print(club_name)
    # club = Club.objects.create()

    tr = soup.select('.lineupBox ul li')

    for line in tr:

        name_em = line.find_all('em')
        for name in name_em:
            print(name.get_text())
