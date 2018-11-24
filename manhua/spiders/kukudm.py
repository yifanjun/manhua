# -*- coding: utf-8 -*-
#这个代码是实现某单个漫画的爬取
import scrapy
import re
from manhua.items import ManhuaItem
from scrapy import Selector

class KukudmSpider(scrapy.Spider):
    name = 'comic'

    def __init__(self):
        #图片链接server域名，这个需要分析js里的src
        self.server_img='http://n5.1whour.com/'
        #章节链接server域名
        self.server_link='http://comic.kukudm.com'
        self.allowed_domains = ['comic.kukudm.com']
        self.start_urls = ['http://comic.kukudm.com/comiclist/2561/index.htm']
        #匹配图片地址的正则表达式（即将js中的“IMG SRC”提取出来）
        self.pattern_img=re.compile(r'\+"(.+)\'>\</a')

    #可以查看scrapy文档
    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0],callback=self.parse1)

    #解析response，获取每个大章节图片链接地址
    def parse1(self, response):
        hxs=Selector(response)
        #章节链接地址
        urls=response.xpath('//dd/a[1]/@href').extract()
        #获取所有的章节名
        dir_names=response.xpath('//dd/a[1]/text()').extract()
        #保存章节链接和章节名
        for index in range(len(urls)):
            item=ManhuaItem()
            item['link_url']=self.server_link+urls[index]
            item['dir_name']=dir_names[index]
            yield scrapy.Request(url=item['link_url'],meta={'item':item},callback=self.parse2)

    #解析一个章节的第一页的页码数和图片链接
    def parse2(self, response):
        #接收传递的item
        item=response.meta['item']
        print(item)
        #下面一句不能少，是用来更新要解析的章节链接
        item['link_url'] = response.url
        print(item)
        hxs=Selector(response)
        #获取章节第一页图片的链接
        pre_img_url=hxs.xpath('//script/text()').extract()
        #举例：http://n5.1whour.com/newkuku/2018/11/20a/转生史莱姆日记_第01话/000122P.jpg
        img_url=(self.server_img+re.search(self.pattern_img,pre_img_url[0]).group(1))
        #将获取的章节的第一页的图片链接保存到img_url中
        item['img_url']=img_url
        #返回item，交给item pipeline下载图片
        yield item
        #获取章节页数
        page_num = hxs.xpath('//td[@valign="top"]/text()').re(u'共(\d+)页')[0]
        #根据页数，整理出本章其他页码链接
        #根据页码规律可知，第一页为 xxx/67046/1.htm 这里处理后面5个变成了xxx/67046/，然后在下面处理链接
        pre_link=item['link_url'][:-5]
        for each_link in range(2,int(page_num)+1):
            #从第二页到最后一页，因为range特性，所以需要+1
            #这里处理上面截取的，第二页就是xxx/67046/2.htm，所以前面要处理一下
            new_link=pre_link+str(each_link)+'.htm'
            yield scrapy.Request(url=new_link,meta={'item':item},callback=self.parse3)

    #解析获得本章节其他页码的图片链接
    def parse3(self, response):
        #接受传递的item
        item=response.meta['item']
        #这一步一定要！不然link_url就会一直是 xxx/67046/1.htm 而不会切换link
        #比如一开始item['link_url']=1.htm，下面这一句就令其变成2.htm，然后依次变3,4,5...
        item['link_url'] = response.url
        #print("要解析的为："+item['link_url'])
        hxs=Selector(response)
        pre_img_url=hxs.xpath('//script/text()').extract()
        img_url = (self.server_img + re.search(self.pattern_img, pre_img_url[0]).group(1))
        #将获取的图片链接保存到img_url中，这里处理的是某章第二页-最后一页的图片链接
        item['img_url']=img_url
        #返回item，交给item pipeline下载图片
        yield item