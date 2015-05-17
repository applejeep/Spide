#-*- coding:utf-8 -*-
import urllib2
import urllib
import cookielib
import re

class DB:
    def __init__(self):
        #self.loginUrl="https://www.douban.com/accounts/login"
        self.loginUrl="https://www.douban.com/accounts/login"
        self.mail="http://www.douban.com/doumail/"
        self.cookies=cookielib.CookieJar()
        self.user_agent='Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers={'User-Agent':self.user_agent}
        self.postdata=urllib.urlencode({
            'form_email':'apple_jeep@163.com',
            'form_password':'' 
        })
        self.opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookies))
        
    def getPage(self):
        request=urllib2.Request(
            url=self.loginUrl,
            data=self.postdata,
            headers=self.headers)
        result=self.opener.open(request)
        print 'login: ', result.read().decode('utf-8')

        result=self.opener.open(self.mail)
        print 'mail: ', result.read().decode('utf-8')
        #print 'response: ', response
    
        

if __name__=="__main__":
    db=DB()
    db.getPage()
