#-*- coding:utf-8 -*-
import urllib2
import urllib
import cookielib
import re

class DB:
    def __init__(self):
        #self.loginUrl="https://www.douban.com/accounts/login"
        self.loginUrl="https://www.douban.com/accounts/login"
        self.cookies=cookielib.CookieJar()
        self.postdata=urllib.urlencode({
            'form_email':'apple_jeep@163.com',
            'form_password':'' 
        })
        self.opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookies))
        
    def getPage(self):
        request=urllib2.Request(
            url=self.loginUrl,
            data=self.postdata)
        result=self.opener.open(request)
        print result.read().decode('utf-8')
        #print 'response: ', response

if __name__=="__main__":
    db=DB()
    db.getPage()
