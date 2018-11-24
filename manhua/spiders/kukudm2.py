# -*- coding: utf-8 -*-
#这个是实现页面多数动漫的爬取
import scrapy
import re
from manhua.items import ManhuaItem
from scrapy import Selector

class Kukudm2Spider(scrapy.Spider):
    name = 'comic2'

    def __init__(self):
        #章节链接server域名
        self.server_link='http://comic.kukudm.com'
        self.allowed_domains = ['comic.kukudm.com']
        self.start_urls = ['http://comic.kukudm.com/comictype/3_1.htm']
        #图片链接server域名，这个需要分析js里的src
        self.server_img='http://n5.1whour.com/'
        #匹配图片地址的正则表达式（即将js中的“IMG SRC”提取出来）
        self.pattern_img=re.compile(r'\+"(.+)\'>\</a')

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0],callback=self.homepage_parse)

    #解析漫画页面，获取所有漫画链接
    def homepage_parse(self, response):
        #获取首页所有的漫画链接和漫画名
        manhua_names=response.xpath('//dd/a[2]/text()').extract()
        manhua_links=response.xpath('//dd/a[2]/@href').extract()

        #循环并解析漫画List，并进入某个具体漫画，进行解析
        for index in range(len(manhua_links)):
            item=ManhuaItem()
            item['manhua_name']=manhua_names[index]
            item['manhua_link']=self.server_link+manhua_links[index]
            #开始分析单章漫画
            yield scrapy.Request(url=item['manhua_link'],meta={'item':item},callback=self.manhua_parse)
        #
        # 抓取下一页，并循环调用来获得所有的漫画
        #PS：如果想爬取所有动漫可以将下面三行去掉注释，然而数量太多不知道要爬到什么时候，所以默认只爬取了第一页的所有动漫
        # next_home_page=self.server_link+response.xpath('//tr[@align="center"]/td/a[contains(text(),"下一页")]/@href').extract()[0]
        # if next_home_page:
        #     yield scrapy.Request(url=next_home_page,callback=self.homepage_parse)

    #解析单个漫画所有章节
    def manhua_parse(self, response):
        item=response.meta['item']
        #漫画章节第一页的链接
        first_urls = response.xpath('//dd/a[1]/@href').extract()
        #循环并解析章节List，并进入章节第一页，进行解析
        for index in range(len(first_urls)):
            item['link_url2']=self.server_link+first_urls[index]
            yield scrapy.Request(url=item['link_url2'], meta={'item':item},callback=self.page_parse)

    #解析某个章节的具体页面，并获取图片地址来源
    def page_parse(self, response):
        item=response.meta['item']
        hxs=Selector(response)
        item['link_url2']=response.url
        #获取本页图片链接，这里获取到的图片链接需要处理一下
        befor_img_url=hxs.xpath('//script/text()').extract()

        #由于不能超过最后一页，因此用到try
        try:
            #说明下为什么在这里解析章节名字。因为如果在manhua_parse就解析dir_name2，会发现后面所有的章节名字都是一样的
            #原因就在于page_parse接受manhua_page的调用，也接受自身循环调用，而每次调用都会传item
            #如果在manhua_page就解析章节名字，那么每次都会被后面的自身调用中的item所覆盖

            #注意！在这里解析章节名字
            dir_name2=response.xpath('//title/text()').extract()[0]
            item['dir_name2']=dir_name2
            #解析并获取本页面图片地址
            img_url = (self.server_img + re.search(self.pattern_img, befor_img_url[0]).group(1))
            item['img_url2'] = img_url
            # 获取下一页图片地址
            befor_next_page_url=response.xpath('//img[@src="/images/d.gif"]/../@href').extract()[0]
            next_page_url=self.server_link+befor_next_page_url
            item['next_page_url']=next_page_url
            yield scrapy.Request(url=next_page_url, meta={'item': item}, callback=self.page_parse)
        except Exception as e:
            print("错误")

        yield item