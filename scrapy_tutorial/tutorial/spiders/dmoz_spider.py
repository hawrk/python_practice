# -*- coding: utf-8 -*-
import scrapy


class DmozSpider(scrapy.spiders.Spider):
    name = "dmoz"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
    ]

    def parse(self, response):
        filename = response.url.split('/')[-2]      #split 分隔后，为 [http://www.dmoz.org,Computers, ...,Python,books, ] 列表组，[-1]为最后的值，
        print ('filename =' + filename)
        with open(filename,'wb') as f:
            f.write(response.body)
