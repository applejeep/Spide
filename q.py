import urllib
import urllib2
import re

page=1
url='http://www.qiushibaike.com/hot/page/'+str(page)
user_agent='Mozilla/5.0 (Windows NT 6.1)'
header={'User-Agent':user_agent}

try:
    request=urllib2.Request(url, headers=header)
    response=urllib2.urlopen(request)
    content=response.read().decode('utf-8')
    #print 'hello'
    #stri='<div.*?class="author.*?>.*?<a.*?</a>.*?<a.*?>(.*?)</a>.*?</div>.*?<div class="content">(.*?)</div>.*?<div(.*?)>'
    #stri='<div\sclass="author">\s<a.*?</a>\s<a.*?>(.*?)</a>.*?</div>.*?<div class="content">(.*?)</div>.*?<div(.*?)>'
    #print stri
    #pattern=re.compile(stri, re.S)
    pattern=re.compile('<div class="content">(.*?)</div>', re.S)
    items=re.findall(pattern,content) 

    for item in items:
        print item.strip()
        #haveImg=re.search("thumb",item[2])
        #if not haveImg:
        #    print item[0].strip()
        #    print item[1].strip()
        #    print 
        
except urllib2.URLError, e:
    if hasattr(e, "code"):
        print e.code
    if hasattr(e, "reason"):
        print e.reason
    
