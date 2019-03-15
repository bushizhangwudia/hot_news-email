# author: zhangwudi
# 2019/3/15 21:35:37

import schedule
import time
from sendEmail import *

address = input("请输入要发送的邮箱:")
send_mail = sendEmail()
send_mail.send_email_weibo(address)
send_mail.send_email_baidu(address)

# 定时每天早上6点发邮件 更多功能请自研究schedule模块
# schedule.every().day.at("6:00").do(send_mail.send_email_weibo(address))
#
# while True:
#     schedule.run_pending()
#     time.sleep(1)