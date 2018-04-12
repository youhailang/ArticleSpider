# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline


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
