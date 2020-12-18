#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# __project__ = XoaMonitor
# __author__ = gaoyuan@donews.com
# __date__ = 2019/12/06
# __time__ = 18:18
"""
发送报警邮件模块
"""
# import email
import smtplib
# from email.MIMEText import MIMEText
from email.mime.text import MIMEText
import optparse


def send_mail(to_str, subject, content):
    admin = "yunwei-monitor@donews.com"
    msg = MIMEText(content, _subtype="html", _charset="utf-8")
    # msg = MIMEText(content, 'plain')
    msg["Subject"] = subject
    msg["From"] = admin
    msg["To"] = to_str
    #  msg["Cc"] = "renren.pe@renren-inc.com"
    try:
        s = smtplib.SMTP()
        s.connect('smtp.exmail.qq.com')
        s.ehlo()
        # s.starttls()
        s.login("yunwei-monitor@donews.com", 'yNE8wZDfYtr65Gra')
        # s.login("yunwei-monitor@donews.com", 'Dn12345')
        s.sendmail(admin, to_str.split(","), msg.as_string())
        s.quit()
    except Exception as e:
        print(str(e))


parser = optparse.OptionParser()
parser.add_option("-t", "", action="store", dest="to")
parser.add_option("-s", "", action="store", dest="subject")
parser.add_option("-c", "", action="store", dest="content")
(options, args) = parser.parse_args()

send_mail(options.to, options.subject, options.content)
