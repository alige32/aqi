# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json

from datetime import datetime


class AqiPipeline(object):
    def process_item(self, item, spider):
        item['time'] = str(datetime.utcnow())
        item['source'] = spider.name
        return item


class AqiJsonPipeline(object):
    def open_spider(self, spider):
        self.f = open("aqi.json", "w")

    def process_item(self, item, spider):
        content = json.dumps(dict(item)) + ",\n"
        self.f.write(content)
        return item

    def close_spider(self, spider):
        self.f.close()
