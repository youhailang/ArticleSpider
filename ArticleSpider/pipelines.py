# -*- coding: utf-8 -*-

import codecs
import datetime
import json

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
from scrapy.exporters import JsonItemExporter
from scrapy.pipelines.images import ImagesPipeline


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


# JsonItemExporter
class JsonExporterPipleline(object):
  # 调用scrapy提供的json export导出json文件
  def __init__(self):
    self.file = open('articleexport.json', 'wb')
    self.exporter = JsonItemExporter(self.file, encoding="utf-8", ensure_ascii=False)
    self.exporter.start_exporting()

  def close_spider(self, spider):
    self.exporter.finish_exporting()
    self.file.close()

  def process_item(self, item, spider):
    self.exporter.export_item(item)
    return item


# 存储到数据库
class MysqlPipeline(object):
  def __init__(self):
    # UnicodeEncodeError: 'latin-1' codec can't encode characters in position 0-7: ordinal not in range(256)
    # 需要加入 charset="utf8", use_unicode=True 参数
    self.conn = MySQLdb.connect('127.0.0.1', 'root', '123456', 'article_spider', charset="utf8", use_unicode=True)
    self.cursor = self.conn.cursor()

  def process_item(self, item, spider):
    insert_sql = """
    insert into jobbole_article(title,url,url_object_id,comment_nums,fav_nums)
    values (%s,%s,%s,%s,%s)
    """
    self.cursor.execute(insert_sql, (
      item['title'], item['url'], item['url_object_id'], item['comment_nums'], item['fav_nums']))
    self.conn.commit()
    return item
