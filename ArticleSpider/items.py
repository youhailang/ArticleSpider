# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import datetime
import re

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join


# 时间转换
def date_convert(value):
  try:
    create_date = datetime.datetime.strptime(value, "%Y/%m/%d").date()
  except Exception as e:
    create_date = datetime.datetime.now().date()
  return create_date


# 获取数字
def get_nums(value):
  match_re = re.match(".*?(\d+).*", value)
  if match_re:
    nums = int(match_re.group(1))
  else:
    nums = 0
  return nums


class ArticlespiderItem(scrapy.Item):
  # define the fields for your item here like:
  # name = scrapy.Field()
  pass


# 通用loader
class ArticleItemLoader(ItemLoader):
  # 自定义itemloader
  default_output_processor = TakeFirst()


# 伯乐在线对应Item
class JobBoleArticleItem(scrapy.Item):
  title = scrapy.Field()
  create_date = scrapy.Field(
    input_processor=MapCompose(date_convert),
  )
  url = scrapy.Field()
  url_object_id = scrapy.Field()
  front_image_url = scrapy.Field(
    output_processor=MapCompose(lambda x: x)
  )
  front_image_path = scrapy.Field()
  praise_nums = scrapy.Field(
    input_processor=MapCompose(get_nums)
  )
  comment_nums = scrapy.Field(
    input_processor=MapCompose(get_nums)
  )
  fav_nums = scrapy.Field(
    input_processor=MapCompose(get_nums)
  )
  tags = scrapy.Field(
    input_processor=MapCompose(lambda x: x if "评论" not in x else ""),
    output_processor=Join(",")
  )
  content = scrapy.Field()
