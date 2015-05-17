import urllib2
import urllib
import re
import os

class Tool:
    removeBr=re.compile('<br><br>|<br>')
    removeElse=re.compile('<.*?>')
    removeNbsp=re.compile('&nbsp;')
    def replace(self, x):
        x=re.sub(self.removeBr,"\n", x)
        x=re.sub(self.removeElse, "", x)
        x=re.sub(self.removeNbsp, "", x)
        return x.strip()

class TaoBao:
    def __init__(self):
        self.siteURL="http://mm.taobao.com/json/request_top_list.htm"
        self.tool=Tool()

    def getPage(self, pageIndex):
        url=self.siteURL+"?"+str(pageIndex)
        #print 'url: ', url
        user_agent='Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers={'User-Agent': user_agent}
        request=urllib2.Request(url, headers=headers)
        response=urllib2.urlopen(request)
        return response.read().decode("gbk")

    def getContents(self, pageIndex):
        page=self.getPage(pageIndex)
        #print 'page: ', page
        patternStr='<div class="personal-info".*?<a href="(.*?)".*?<img src="(.*?)".*?<a class="lady-name".*?>(.*?)</a>.*?<strong>(.*?)</strong>.*?<span>(.*?)</span>'
        pattern=re.compile(patternStr, re.S)
        items=re.findall(pattern, page)

        contents=[]
        for item in items:
            contents.append([item[0],item[1],item[2],item[3],item[4]])
            #print item[0],item[1],item[2],item[3],item[4]
        return contents
    
    def getDetailPage(self, infoURL):
        request=urllib2.Request(infoURL)
        response=urllib2.urlopen(request)
        return response.read().decode('gbk')

    def getBrief(self, page):
        pattern=re.compile('<div class="mm-aixiu-content".*?>(.*?)<!--',re.S)
        result=re.search(pattern, page)
        return self.tool.replace(result.group(1))

    def getAllImg(self, page):
        pattern=re.compile('<div class="mm-aixiu-content".*?>(.*?)<!--',re.S)
        content=re.search(pattern, page)
        patternImg=re.compile('<img.*?src="(.*?)"/>', re.S)
        images=re.findall(patternImg, content.group(1))
        return images
       
    def saveImgs(self, images, name):
        number=1
        for imgURL in images:
            splitPath=imgURL.split('.')
            fTail=splitPath.pop()
            fileName=name+"/"+str(number)+"."+fTail
            self.saveImg(imgURL, fileName)
            number+=1
    
    def saveIcon(self, iconURL, name):
        splitPath=iconURL.split('.')
        fTail=splitPath.pop()
        fileName=name+'/icon.'+fTail
        self.saveImg(iconURL, fileName)
    
    def saveBrief(self, content, name):
        fileName=name+"/"+name+".txt"
        f=open(fileName, "w+")
        f.write(content.encode('utf-8'))

    def saveImg(self, imgURL, fileName):
        u=urllib.urlopen(imgURL)
        data=u.read()
        f=open(fileName, 'wb')
        f.write(data)
        f.close()

    def mkdir(self, path):
        os.mkdir(path)
        #path=path.strip()
        #isExists=os.path.exists(path)
        #if not isExists:
        #    os.mkdirs(path)
        #    return True
        #else:
        #    return False

    def savePageInfo(self, pageIndex):
        contents=self.getContents(pageIndex)
        for item in contents:
            detailURL=item[0]

            #print 'detailURL: ', detailURL
            detailPage=self.getDetailPage(detailURL)
            #print 'detailPage: ', detailPage
            brief=self.getBrief(detailPage)
            images=self.getAllImg(detailPage)
            #print 'item[2]: ', item[2]

            self.mkdir(item[2])

            self.saveBrief(brief, item[2])
            self.saveIcon(item[1], item[2])
            self.saveImgs(images, item[2])

    def savePagesInfo(self, start, end):
        for i in range(start, end+1):
            self.savePageInfo(i)

spide=TaoBao()
spide.savePageInfo(1)
#spide.getContents(2)
