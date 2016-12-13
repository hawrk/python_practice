import urllib.request
import gzip
import re
import urllib.parse
from bs4 import BeautifulSoup

headers = {
    'Connection': 'Keep-Alive',
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate,br',
    'Host': 'blog.csdn.net',
    'DNT': '1'
}

def unzip(data):
    try:
        data = gzip.decompress(data)
    except:
        print ("decompress fail...")
    return data

def saveFile(data):
    path = "/home/hawrk/PycharmProjects/scrapy/csdn_title_bs4.txt"
    file = open(path,'ab')
    for d in data:
        d = str(d) + '\n'
        file.write(d.encode('gbk'))

    file.close()

class CSDNSpider:
    def __init__(self,pageIdx = 1,url = 'http://blog.csdn.net/fly_yr/article/list/1'):
        self.pageIdx = pageIdx
        self.url = url[0:url.rfind('/') + 1] + str(pageIdx)

    def getPage(self):
        req = urllib.request.Request(url = self.url,headers = headers)
        res = urllib.request.urlopen(req)

        data = res.read()
        data = unzip(data)
        data = data.decode('utf-8')

        soup = BeautifulSoup(data,'html5lib')
        tag = soup.find('div',"pagelist")
        pagesdata = tag.span.get_text()
        pattern = r'共(.*?)页'
        pagesNum = re.findall(re.compile(pattern),pagesdata)[0]
        print ("pageNum = ",pagesNum)

        return pagesNum

    def setPage(self,idx):
        self.url = self.url[0:self.url.rfind('/') + 1] + str(idx)
        print ('url = [%s]' %self.url)

    def readData(self):
        print ("into read data url:[%s]" %self.url)
        ret = []
        req = urllib.request.Request(url = self.url,headers = headers)
        res = urllib.request.urlopen(req)

        data = res.read()
        data = unzip(data)
        data = data.decode('utf-8')

        soup = BeautifulSoup(data,'html5lib')
        items = soup.find_all('div','list_item article_item')
        for item in items:
            title = item.find('span','link_title').a.get_text().strip()
            link = item.find('span','link_title').a.get('href').strip()
            print ("title = [%s]" %title)
            print ("link = [%s]" %link)
            ret.append("title =" + title + '\n'+ " link =" + link)

        return ret

cs = CSDNSpider()
pageNum = int(cs.getPage())
print ('pageNum = %d' %pageNum)

for idx in range(pageNum):
    cs.setPage(idx)
    papers = cs.readData()
    saveFile(papers)

