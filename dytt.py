# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 20:40:16 2018

@author: eric.li
"""
import requests
from bs4 import BeautifulSoup
import re
import time

dytt = r'http://www.dytt8.net/html/gndy/dyzz/index.html'
dytt_head = r'http://www.dytt8.net'
dytt_backup = r'http://www.dytt8.net/html/gndy/dyzz/'

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36"}


def getHTML(url):
    try:
        #大批次访问，设置访问session
        requests.adapters.DEFAULT_RETRIES = 5
        response = requests.session()
        response.keep_alive = False
        response = response.get(url, headers = headers, timeout = 5)
        #print(response.apparent_encoding) #gb2312
        #从默认的unicode转码为gb2312
        response.encoding = 'gb2312'
        return response.text
    except :
        print('session timeout')

def getContent(html):
    soup = BeautifulSoup(html, 'lxml')
    
    #newLinkList -> 电影标题，超链接
    newLinkList = soup.find_all('a', attrs = {'class', 'ulink'}, text = re.compile(r'^[0-9]'))
#    print(newLinkList[0].text, newLinkList[0]['href'])  #2018年动作《贼巢 未分级加长版》BD中英双字幕 /html/gndy/dyzz/20180417/56720.html
    
    updateDate = soup.find_all('font', text = re.compile(r'^日期'))
#    print(updateDate[len(updateDate)-1].text)  #日期：2018-04-17 18:06:08 点击：0 
     
    #电影简介
    briefIntroduction = soup.find_all('td', colspan = '2', style = re.compile(r'^padding'))
#    print(briefIntroduction[0].text)   #贼巢 未分级加长版
    
#    for newMoviePage in newLinkList:
#        newPageUrl = newMoviePage['href']
#        getHTML(newPageUrl)
    
    #校验是否有下一页
    hasNextPage = soup.find('a', text = re.compile('下一页'))
#    print(hasNextPage)
    if hasNextPage:
        nextPage = dytt_backup + hasNextPage['href']
#        print(nextPage)
        return newLinkList, updateDate, briefIntroduction, nextPage
    return newLinkList, updateDate, briefIntroduction, None
    
def getDownloadUrl(url):
    html = getHTML(url)
    soup = BeautifulSoup(html, 'lxml')
    downloadUrl = soup.find('td', style = re.compile('WORD-WRAP: break-word'))
    if not downloadUrl:
        return ''
#    print(downloadUrl['href'])
    return downloadUrl.find('a')['href']
    
def main():
    d = dytt
    i = 0
    html = getHTML(d)
    a, b, c, d = getContent(html)
    for i in range(0,len(a)):
        str1 = dytt_head + a[i]['href']
        downloadUrl = getDownloadUrl(str1)
        with open(r'D:\files_io_for_test\dytt.txt', 'a', encoding = 'utf-8') as f:
            f.write(a[i].text.replace('\n', ''))
            f.write('   $   ')
            f.write(b[i].text.replace('\n', ''))
            f.write('   $   ')
            f.write(c[i].text.replace('\n', ''))
            f.write('   $   ')
            f.write(downloadUrl)
            f.write('\n')
        time.sleep(1)
#    while d:
#        html = getHTML(d)
#        a, b, c, d = getContent(html)
#        for i in range(0,len(a)): 
#            str1 = dytt_head + a[i]['href']
#            print(str1)
#            downloadUrl = getDownloadUrl(str1)
#            time.sleep(1)
#            print(a[i].text) #09最新惊悚大片《地铁惊魂/骑劫地下铁》R5中字
#            print(dytt_head + a[i]['href']) #http://www.dytt8.net/html/gndy/dyzz/20091004/22009.html
#            print(downloadUrl['href'])
#            print(b[i].text) # 日期：2009-10-04 00:00:19 点击：65295
#            print(c[i].text) #◎译 名 地铁惊魂/骑劫地下铁
#            print(d) #http://www.dytt8.net/html/gndy/dyzz/list_23_173.html
#            print('\n')
#            with open(r'D:\files_io_for_test\dytt.txt', 'a', encoding = 'utf-8') as f:
#                f.write(a[i].text.replace('\n', ''))
#                f.write('   $   ')
#                f.write(b[i].text.replace('\n', ''))
#                f.write('   $   ')
#                f.write(c[i].text.replace('\n', ''))
#                f.write('   $   ')
#                f.write(downloadUrl)
#                f.write('\n')
#        time.sleep(1)
        
if __name__ == '__main__':
    main()
#    html = getHTML(r'http://www.dytt8.net/html/gndy/dyzz/list_23_40.html')
#    a, b, c, d = getContent(html)
#    print(len(a), len(b), len(c), len(d))
#    for i in range(0,len(a)):
#        downloadUrl = getDownloadUrl(dytt_head + a[i]['href'])
#        print(a[i].text)
#        print(a[i]['href'])
#        print(downloadUrl['href'])
#        print(b[i].text.replace('\n', ''))
#        print(c[i].text)
#        print(d)
#        print(i)
#        print('\n')
#        with open(r'D:\files_io_for_test\dytt.txt', 'a', encoding = 'utf-8') as f:
#            f.write(a[i].text.replace('\n', ''))
#            f.write('   $   ')
#            f.write(b[i].text.replace('\n', ''))
#            f.write('   $   ')
#            f.write(c[i].text.replace('\n', ''))
#            f.write('   $   ')
#            f.write(downloadUrl['href'])
#            f.write('\n')






