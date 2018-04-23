#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 21 14:03:26 2018

@author: eric.li
"""

from bs4 import BeautifulSoup
import requests
import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
import os

sender = r'xxx@qq.com'
password = 'xxx' #设置SMTP时获得的16位字符码
mail_host = 'smtp.qq.com'
receivers = ['xxx1@qq.com', 'xxx2@qq.com', 'xxx3@qq.com']
headers = {r'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36'}
oneUrl = r'http://wufazhuce.com/#carousel-one'
path = '/home/yituadmin/Personal_Eric/oneforeveryday/oneImage'
emailTitle = 'One [一个] -- 每天只为你准备一张图片、一篇文字和一个问答'

def getHTML(url):
    response = requests.get(url, headers = headers)
    response.encoding = 'utf-8'
    soup = getSoup(response.text)
    return soup

def getSoup(html):
    return BeautifulSoup(html, 'lxml')

def getContent(soup):
    i = 0
    strkanhao = ''
    kanhao = soup.find('div', 'fp-one-titulo-pubdate').find_all('p')
    for i in range(0, len(kanhao)):
        strkanhao = strkanhao + kanhao[i].text
        if not i == len(kanhao)-1:
            strkanhao = strkanhao + ' _'
#    print(strkanhao)
    
    neirong = soup.find('div', 'fp-one-cita').find('a').text
#    print(neirong)
    
    peitu = soup.find('img', 'fp-one-imagen')['src']
#    print(peitu)
    
    return strkanhao, neirong, peitu

def saveImageToLocal(imageName, imageUrl):
    byteImage = requests.get(imageUrl)
    if not os.path.exists(path):
        os.mkdir(path)
    localPath = path + r'/' + imageName + '.jpg'   
    with open(localPath, 'wb') as img:
        img.write(byteImage.content)
    return localPath

def sending_email(kanhao, emailContent, localImagePath):
    #设置email信息
    msg = MIMEMultipart('related')
    #邮件主题
    msg['Subject'] = emailTitle
    
    #发送方信息
    msg['From'] = sender
    msg_content = '刊号' + kanhao + '\n' + emailContent
    msg.attach(MIMEText(msg_content, 'plain', 'utf-8'))
    with open(localImagePath, 'rb') as f:
        # 设置附件的MIME和文件名，这里是jpg类型,可以换png或其他类型:
        mime = MIMEBase('image', 'png', filename='oneImage.png')
        # 加上必要的头信息:
        mime.add_header('Content-Disposition', 'attachment', filename='oneImage.png')
        mime.add_header('Content-ID', '<0>')
        mime.add_header('X-Attachment-Id', '0')
        # 把附件的内容读进来:
        mime.set_payload(f.read())
        # 用Base64编码:
        encoders.encode_base64(mime)
        # 添加到MIMEMultipart:
        msg.attach(mime)
    #登录并发送邮件
    try:
        #QQsmtp服务器的端口号为465或587
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)
        s.set_debuglevel(1)
        s.login(sender,password)
        #给receivers列表中的联系人逐个发送邮件
        for item in receivers:
            msg['To'] = to = item
            s.sendmail(sender,to,msg.as_string())
            print('Success!')
        s.quit()
        print ("All emails have been sent over!")
    except smtplib.SMTPException as e:
        print ("Falied,%s",e)

def main():
    soup = getHTML(oneUrl)
    strkanhao, neirong, peitu = getContent(soup)
    localImagePath = saveImageToLocal(strkanhao, peitu)
    sending_email(strkanhao, neirong, localImagePath)

if __name__ == '__main__':
    main()