# -*- coding: utf-8 -*-

import codecs
import json

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
import datetime


class CJsonEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, datetime.datetime):
      return obj.strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(obj, datetime.date):
      return obj.strftime("%Y-%m-%d")
    else:
      return json.JSONEncoder.default(self, obj)


class ArticlespiderPipeline(object):
  def process_item(self, item, spider):
    return item


# 自定义图片处理
class ArticlesImagePipeline(ImagesPipeline):
  def item_completed(self, results, item, info):
    for ok, value in results:
      front_image_path = value['path']
    item['front_image_path'] = front_image_path
    return item


class JsonWithEncodingPipeline(object):
  def __init__(self):
    self.file = codecs.open('article.json', 'w', encoding="utf-8")

  def process_item(self, item, spider):
    lines = json.dumps(dict(item), ensure_ascii=False, cls=CJsonEncoder) + "\n"
    self.file.write(lines)
    return item

  def spider_closed(self, spider):
    self.file.close()
