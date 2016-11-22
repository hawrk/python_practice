import urllib.request
import gzip
import re
import http.cookiejar
import urllib.parse

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


pages = r'<div.*?pagelist">.*?<span>.*?共(.*?)页</span>'


class CSDNSpider:
    def __init__(self,pageIdx = 1,url = 'http://blog.csdn.net/fly_yr/article/list/1'):
        self.pageIdx = pageIdx
        self.url = url[0:url.rfind('/') + 1] + str(pageIdx)

    def setPage(self,idx):
        self.url = self.url[0:self.url.rfind('/') + 1] + str(idx)
        print ('url = [%s]' %self.url)

    def readData(self):
        print ("into read data url:[%s]" %self.url)
        ret = []
        str = r'<div.*?link_title.*?a href=".*?">(.*?)</a></span>'

        req = urllib.request.Request(url = self.url,headers = headers)
        res = urllib.request.urlopen(req)

        data = res.read()
        data = unzip(data)
        data = data.decode('utf-8')
        pattern = re.compile(str,re.DOTALL)
        items = re.findall(pattern,data)
        for item in items:
            title = item.strip()
            print ('title = [%s]' %title)
            ret.append(title)

        return ret

    def getPages(self):
        req = urllib.request.Request(url=self.url,headers=headers)
        res = urllib.request.urlopen(req)

        data = res.read()
        data = unzip(data)
        data = data.decode('utf-8')

        pages = r'<div.*?pagelist">.*?<span>.*?共(.*?)页</span>'
        pattern = re.compile(pages,re.DOTALL)
        pageNum = re.findall(pattern,data)[0]     #取第一个正则（.*?)分组 即 共 页中的所有内容

        return pageNum


if __name__ == '__main__':
    cs = CSDNSpider()
    pageNum = int(cs.getPages())
    print ('page Num = [%s]' %pageNum)

    for idx in range(pageNum):
        cs.setPage(idx+1)
        print ('current page:', idx+1)
        papers = cs.readData()
