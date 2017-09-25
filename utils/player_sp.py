#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Date: 2017/9/25


import urllib.request
import http.cookiejar
from bs4 import BeautifulSoup

# 图片地址

num = 0
# 发出请求
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}


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


zuqiu_url = 'http://saishi.caipiao.163.com/9/0000.html'
oper = makeMyOpener()
m_request = oper.open(zuqiu_url, timeout=2)
# 获取返回结果
m_data1 = m_request.read().decode('utf-8')

soup = BeautifulSoup(m_data1, 'html.parser')
# print(soup.title)
# print(soup.prettify())
tr = soup.select('#scoreLive tr td')

for line in tr:

    a = line.find_all('td')
    # print(len(a),a)
    try:
        for i in [1, 3, 5, 6, 7]:
            b = a[i].get_text().strip()
            print(str(b).strip().replace(' ', '').replace('\r\n', ''), end='-')
        print('')
    except Exception as a:
        pass
        # ss = BeautifulSoup(line, 'html.parser')
        # for i in ss.select('.texRight a'):
        #     print(i.get_text().strip())
        #     linkre = re.compile(r'alt="(\w*?)".*?src="(.+?)"')

        # 关闭文件


