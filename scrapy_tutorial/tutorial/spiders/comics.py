# -*- coding: utf-8 -*-

import urllib
import urllib2
import scrapy
import os
import zlib

# http://www.jianshu.com/p/c1704b4dc04d?hmsr=toutiao.io&utm_medium=toutiao.io&utm_source=toutiao.io

from bs4 import BeautifulSoup


def save_file(self, path):
    tar_path = 'carton_pic'
    if not os.path.isdir(tar_path):
        os.mkdir(tar_path)
    pos = path.rindex('/')
    t = os.path.join(tar_path, path[pos + 1:])
    return t

class Comics(scrapy.Spider):
    name = "comics"

    def start_requests(self):     #重载父类的方法
        urls = ['http://www.xeall.com/shenshi']
        for url in urls:
            yield scrapy.Request(url=url,callback=self.parse)

    #或者可以直接用  start_urls

    def parse(self, response):
        #self.log(response.body)
        content = response.body
        if not content:
            self.log('parse body fail')
            return
        #返回内容用 beautifusoup解析
        soup = BeautifulSoup(content,"html5lib")

        #图集列表
        listcon_tag = soup.find('ul',class_="listcon")  # <ul class = "pic listcon">...</ul>
        #每部漫画的标签链接
        com_a_list = listcon_tag.find_all('a', attrs={'href': True})

        #获取所有漫画的url
        comics_url_list = []
        base = 'http://www.xeall.com'
        for tag_a in com_a_list:
            url = base + tag_a['href']
            comics_url_list.append(url)

        print ('\n>>>>>>>>current page list<<<<<<<<<<<<')
        #print(comics_url_list)

        #处理当前页每部漫画
        for url in comics_url_list:
            print ('>>>>>parse comics:' + url)
            yield scrapy.Request(url=url,callback=self.comics_parse)

        #先get 第一部
        return

    #异步回调函数,处理每部漫画的url
    def comics_parse(self,response):
        #提取每部漫 画的数据
        content = response.body
        if not content:
            self.log("parse comics body error")
            return

        #beautifulsop
        soup = BeautifulSoup(content,"html5lib")

        #get 页数标签
        page_list_tag = soup.find('ul',class_='pagelist')
        #当前页数
        current_li = page_list_tag.find('li',class_='thisclass')
        page_num = current_li.a.string
        self.log('current page=' + page_num)

        #获取当前图片url
        li_tag = soup.find('li',id='imgshow')
        img_tag = li_tag.find('img')
        img_url = img_tag['src']
        self.log("img url = " + img_url)

        #漫画标题
        title = img_tag['alt']

        #save
        self.save_img(page_num,title,img_url)

        #next pic
        a_tag_list = page_list_tag.find_all('a')
        next_page = a_tag_list[-1]['href']
        if next_page == '#':
            self.log('parse:'+title+'finish')
        else:
            next_page = 'http://www.xeall.com/shenshi/' + next_page
            yield scrapy.Request(next_page,callback=self.comics_parse)

    def save_img(self, img_mun, title, img_url):
        # 将图片保存到本地
        self.log('saving pic: ' + img_url)

        # 保存漫画的文件夹
        document = '/home/hawrk/tutorial/tutorial/spiders/cartoon'

        # 每部漫画的文件名以标题命名
        comics_path = document + '/' + title
        exists = os.path.exists(comics_path)
        if not exists:
            self.log('create document: ' + title)
            os.makedirs(comics_path)

        # 每张图片以页数命名
        pic_name = comics_path + '/' + img_mun + '.jpg'

        # 检查图片是否已经下载到本地，若存在则不再重新下载
        exists = os.path.exists(pic_name)
        if exists:
            self.log('pic exists: ' + pic_name)
            return

        try:
            user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
            headers = {'User-Agent': user_agent}

            req = urllib2.Request(img_url,headers=headers)
            response = urllib2.urlopen(req,timeout=30)
            #req = urllib.request.Request(img_url, headers=headers)
            #response = urllib.request.urlopen(req, timeout=30)

            # 请求返回到的数据
            data = response.read()

            # 若返回数据为压缩数据需要先进行解压
            if response.info().get('Content-Encoding') == 'gzip':
                data = zlib.decompress(data, 16 + zlib.MAX_WBITS)

            # 图片保存到本地
            fp = open(pic_name, "wb")
            fp.write(data)
            fp.close

            self.log('save image finished:' + pic_name)

        # urllib.request.urlretrieve(img_url, pic_name)
        except Exception as e:
            self.log('save image error.')
            self.log(e)

