#!/usr/bin/python
# -*- coding: UTF-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import os
import sys
path = os.getcwd().split('cassia_automation')[0] + 'cassia_automation/lib/'
sys.path.append(path)
from tools import read_config

conf = read_config()['mail_attr']


class send_report():

    def __init__(self, comment):
        self.mail_host = conf['mail_host']
        self.mail_port = conf['mail_port']
        self.mail_user = conf['mail_user']
        self.mail_pass = conf['mail_pass']
        self.mail_sender = conf['mail_sender']
        self.mail_recv = eval(conf['mail_recv'])
        self.mail_text = comment

    def write_mail(self):
        # 创建一个带附件的实例
        self.message = MIMEMultipart()
        self.message['From'] = Header("自动化测试平台", 'utf-8')
        self.message['To'] = Header(",".join(self.mail_recv), 'utf-8')
        subject = '自动化测试平台 测试报告'
        self.message['Subject'] = Header(subject, 'utf-8')

        # 邮件正文内容
        self.message.attach(MIMEText(self.mail_text, 'plain', 'utf-8'))

        # 添加附件
        path = os.getcwd().split('cassia_automation')[
            0] + 'cassia_automation/reports/'
        reports = sorted(os.listdir(path), reverse=True)
        report = path + reports[0]
        att1 = MIMEText(open(report, 'rb').read(), 'base64', 'utf-8')
        att1["Content-Type"] = 'application/octet-stream'
        # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
        att1["Content-Disposition"] = 'attachment; filename=%s' % reports[0]
        self.message.attach(att1)

    def send(self):
        self.write_mail()
        try:
            smtpObj = smtplib.SMTP_SSL(self.mail_host, self.mail_port)
            smtpObj.login(self.mail_user, self.mail_pass)
            smtpObj.sendmail(self.mail_sender, self.mail_recv,
                             self.message.as_string())
            print("邮件发送成功")
        except smtplib.SMTPException as e:
            print("Error: 无法发送邮件", e)


if __name__ == '__main__':
    send_report('abc').send()
