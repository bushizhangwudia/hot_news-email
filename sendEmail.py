#!/usr/bin/python3
# author: zhangwudi
# 2019/3/15 21:35:37
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from pprint import pprint

import requests
from bs4 import BeautifulSoup
from urllib import parse


class sendEmail:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36"
        }
        self.mail_host = "smtp.mxhichina.com"  # 邮箱服务器服务器
        self.mail_user = "wangli@conforx.com"  # 邮箱账号
        self.mail_pass = "*******"  # 邮箱授权码

    def send_email_baidu(self, email):
        # 抓取百度热搜信息
        f = requests.get('http://top.baidu.com/buzz?b=1', headers=self.headers).text.encode('latin-1').decode('GBK')
        soup = BeautifulSoup(f, features="lxml")
        list_tag = soup.find(attrs={"class", "mainBody"}).find(attrs={"class", "list-table"})
        trs = list_tag.find_all('tr')
        json_str_baidu = {}
        mail_msg = ''
        for i in range(1, 10):
            tr = trs[i]
            if tr.get('class') is not None:
                if tr.get('class')[0] == 'item-tr':
                    continue
            tds = tr.find_all('td')
            keyword = tds[1]
            word = keyword.text.replace('search', '').strip()
            json_str_baidu[word] = 'https://www.baidu.com/s?wd=' + parse.quote(word)
            mail_msgone = """
            <p>%s:<a href="'%s'">链接</a></p>
                 """ % (word, json_str_baidu)
            mail_msg = mail_msg + mail_msgone
        # 写入邮箱并发送
        sender = 'wangli@conforx.com'
        receivers = email  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
        message = MIMEText(mail_msg, 'html', 'utf-8')
        subject = 'zhangwudi-❥(^_-)'
        message['Subject'] = Header(subject, 'utf-8')
        try:
            smtpObj = smtplib.SMTP()
            smtpObj.connect(self.mail_host, 25)  # 25 为 SMTP 端口号
            smtpObj.login(self.mail_user, self.mail_pass)
            smtpObj.sendmail(sender, receivers, message.as_string())
            print("邮件发送成功")
        except Exception as e:
            print("Error: 无法发送邮件")
            print(e)

    def send_email_weibo(self, email):
        # 抓取微博热搜话题
        html_doc = requests.get("https://s.weibo.com/top/summary?cate=realtimehot", headers=self.headers).text
        soup = BeautifulSoup(html_doc, features="lxml")
        tags = soup.select('.td-02')
        json_str_weibo = {}
        mail_msg = ''
        for tag in tags:
            json_str_weibo[tag.find('a').text] = 'https://s.weibo.com' + tag.find('a')['href']
            mail_msgone = """
                        <p>%s:<a href="'%s'">链接</a></p>
                             """ % (tag.find('a').text, json_str_weibo[tag.find('a').text])
            mail_msg = mail_msg + mail_msgone
        # 写入邮箱文本并发送
        sender = 'wangli@conforx.com'
        receivers = email
        message = MIMEText(mail_msg, 'html', 'utf-8')
        subject = 'zhangwudi-❥(^_-)'
        message['Subject'] = Header(subject, 'utf-8')
        try:
            smtpObj = smtplib.SMTP()
            smtpObj.connect(self.mail_host, 25)  # 25 为 SMTP 端口号
            smtpObj.login(self.mail_user, self.mail_pass)
            smtpObj.sendmail(sender, receivers, message.as_string())
            print("邮件发送成功")
        except Exception as e:
            print("Error: 无法发送邮件")
            print(e)
