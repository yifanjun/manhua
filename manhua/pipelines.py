# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import requests
from manhua import settings
from scrapy import Request

# #kukudm处理获取的链接并下载
# class ManhuaPipeline(object):
#     def process_item(self, item, spider):
#     	#如果获取了图片链接，做如下操作
#         if 'img_url' in item:
#             images=[]
#             #文件夹的名字 F:/转生史莱姆/章节名
#             dir_path='%s/%s' % (settings.IMAGES_STORE,item['dir_name'])
#             #文件不存在则创建文件夹
#             if not os.path.exists(dir_path):
#                 os.makedirs(dir_path)
#             #解析链接，根据链接为图片命名
#             #http://n5.1whour.com/newkuku/2018/11/20a/xxx/00080TK.jpg
#             page=item['link_url'].split('/')[-1].split('.')[0]
#             #图片名
#             image_file_name='第'+page+'页.jpg'
#             #图片保存路径 F:/转生史莱姆/章节名/page.jpg
#             file_path='%s/%s' % (dir_path,image_file_name)
#             images.append(file_path)
#             print(item)
#             print(file_path)
#             #抓取图片
#             with open(file_path,'wb') as fp:
#                 response=requests.get(url=item['img_url'])
#                 for block in response.iter_content(1024):
#                     if not block:
#                         break
#                     fp.write(block)
#
#             #返回图片保存路径
#             item['image_paths']=images


#kukudm2处理获取的链接并下载
class ManhuaPipeline2(object):
    def process_item(self, item, spider):
    	#如果获取了图片链接，做如下操作
        print(item['img_url2'])
        if 'img_url2' in item:
            images=[]
            #文件夹的名字 F:/kukudm/漫画名字/章节名
            dir_path='F://kukudm//%s/%s' % (item['manhua_name'],item['dir_name2'])
            #文件不存在则创建文件夹
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            #解析链接，根据链接为图片命名
            #http://n5.1whour.com/newkuku/2018/11/20a/xxx/00080TK.jpg
            page=item['link_url2'].split('/')[-1].split('.')[0]
            #图片名
            image_file_name='第'+page+'页.jpg'
            #图片保存路径 F:/转生史莱姆/章节名/page.jpg
            file_path='%s/%s' % (dir_path,image_file_name)
            images.append(file_path)
            #抓取图片
            with open(file_path,'wb') as fp:
                response=requests.get(url=item['img_url2'])
                for block in response.iter_content(1024):
                    if not block:
                        break
                    fp.write(block)

            #返回图片保存路径
            item['image_paths']=images