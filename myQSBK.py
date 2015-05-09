#-*- coding: utf-8 -*-
import urllib2
import urllib
import re
import thread
import time

class QSBK:
    def __init__(self):
        self.page=1
        self.pages=[]
        self.enable=False
    
    def GetPage(self, page):
        myUrl="http://www.qiushibaike.com/hot/page/"+page
        user_agent='Mozilla/5.0 (Windows NT 6.1)'
        header={'User-Agent':user_agent}

        req=urllib2.Request(myUrl, headers=header)
        myResponse=urllib2.urlopen(req)
        content=myResponse.read().decode('utf-8')

        pattern=re.compile('<div class="content">(.*?)</div>', re.S)
        myitems=re.findall(pattern, content)
        #self.pages.append(myitems)
        return myitems
        
    def LoadPage(self):
        while self.enable:
            if(len(self.pages))<2:
                #print 'self.page', self.page
                myPage=self.GetPage(str(self.page))
                self.page+=1
                self.pages.append(myPage)
            else:
                time.sleep(1)

    def ShowPage(self, nowPage, page):
        for item in nowPage:
            print 'page %d:'%page, item.strip()
            myInput=raw_input()
            if myInput=='q':
                self.enable=False
                break;

    def start(self):
        self.enable=True
        page=self.page
        
        thread.start_new_thread(self.LoadPage,())
        while self.enable:
            if self.pages:
                nowPage=self.pages[0]
                del self.pages[0]
                self.ShowPage(nowPage, page)
                page+=1
        
if __name__=="__main__":
    print u"""
        the program:baike
        """
    print 'enter enter'
    raw_input(' ')
    myModel=QSBK()
    myModel.start()
    #myModel.GetPage(str(1))

