# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
class ManhuaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #章节名
    dir_name=scrapy.Field()
    #章节链接，即每章第一页链接
    link_url=scrapy.Field()
    #图片来源链接
    img_url=scrapy.Field()
    image_paths=scrapy.Field()