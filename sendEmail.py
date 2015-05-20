#-*- coding:utf-8-*-
import smtplib
from email.mime.text import MIMEText

def sendEmail(msg):
    _user = raw_input("Email: ")
    _pwd  = raw_input("Password: ")
    _to   = raw_input("To Email: ")
    
    ####使用MIMEText构造符合smtp协议的header及body
    #msg = MIMEText("乔装打扮，不择手段")
    msg = MIMEText(msg)
    msg["Subject"] = "don't panic"
    msg["From"]    = _user
    msg["To"]      = _to
    
    #s = smtplib.SMTP("smtp.qq.com", timeout=30)#连接smtp邮件服务器,端口默认是25
    s = smtplib.SMTP("smtp.163.com", timeout=30)#连接smtp邮件服务器,端口默认是25
    s.login(_user, _pwd)#登陆服务器
    s.sendmail(_user, _to, msg.as_string())#发送邮件
    s.close()

if __name__=="__main__":
    sendEmail("中国")
    sendEmail("aaa")
