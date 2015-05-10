import urllib2
import urllib
import re

class Tool:
    removeBr=re.compile('<br><br>|<br>')
    removeElse=re.compile('<.*?>')
    def replace(self, x):
        x=re.sub(self.removeBr,"\n", x)
        x=re.sub(self.removeElse, "", x)
        return x.strip()

class BDTB:
    def __init__(self, baseUrl, seeLZ):
        self.baseURL=baseUrl
        self.seeLZ=seeLZ
        self.file=None
        self.floor=1
        self.tool=Tool()
        self.defaultTile=u"tieba"

    def getPage(self, pageNum):
        url=self.baseURL+'?see_lz='+str(self.seeLZ)+'&pn='+str(pageNum)
        req=urllib2.Request(url)
        response=urllib2.urlopen(req)
        return response.read().decode('utf-8')

    def getTitle(self, page):
        pattern=re.compile('<h1\sclass="core_title_txt.*?>(.*?)</h1>', re.S)
        return re.search(pattern, page).group(1).strip()
        
    def getPageNum(self, page):
        pattern=re.compile('<span\sclass="red">(.*?)</span>', re.S)
        return re.search(pattern, page).group(1).strip() 

    def getContent(self, page):
        pattern=re.compile('<div id="post_content_.*?>(.*?)</div>', re.S)
        items=re.findall(pattern, page)
        contents=[]
        for item in items:
            content="\n"+self.tool.replace(item)+"\n"
            contents.append(content.encode('utf-8')) ######
        return contents

    def setFileTitle(self, title):
        if title is not None:
            self.file=open(title+".txt", "w+")
        else:
            self.file=open(self.defaultTitle+".txt", "w+")
    
    def writeData(self,contents):
        for item in contents:
            floorLine="\n"+str(self.floor)+u"----------------------------------------------------\n"
            self.file.write(floorLine)
            self.file.write(item)
            self.floor+=1
    
    def start(self):
        indexPage=self.getPage(1)
        pageNum=self.getPageNum(indexPage)
        title=self.getTitle(indexPage)
        self.setFileTitle(title)
        if pageNum==None:
            return
        print "", pageNum

        for i in range(1, int(pageNum)+1):
            print "", i
            page=self.getPage(i)
            contents=self.getContent(page)
            self.writeData(contents)

if __name__=="__main__":
    baseURL='http://tieba.baidu.com/p/3138733512'
    seeLZ=0
    bdtb=BDTB(baseURL, seeLZ) 
    bdtb.start()
