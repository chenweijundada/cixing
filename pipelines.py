# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json

from jingdong_scrapy.jingdong import settings

class JingdongPipeline(object):

    def __init__(self):
        self.file = open('ak17.json', 'a')  # 存储文件的类型

    def process_item(self, item, spider):
        result = json.dumps(dict(item), ensure_ascii=False) + ', \n'
        self.file.write(result)
        return item

    def close_spider(self, spider):
        self.file.close()
