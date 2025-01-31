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

from settings import SQL_DATETIME_FORMAT
# 时间转换
from utils.common import cutils
from w3lib.html import remove_tags


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

  def get_insert_sql(self):
    insert_sql = """
      insert into jobbole_article(title,create_date,url,url_object_id,front_image_url,front_image_path,comment_nums,fav_nums,praise_nums,tags,content)
      values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
      """
    params = (
      self['title'], self['create_date'], self['url'], self['url_object_id'], self['front_image_url'],
      self['front_image_path'], self['comment_nums'], self['fav_nums'], self['praise_nums'], self['tags'],
      self['content'])
    return insert_sql, params


# 知乎的问题 item
class ZhihuQuestionItem(scrapy.Item):
  zhihu_id = scrapy.Field()
  topics = scrapy.Field()
  url = scrapy.Field()
  title = scrapy.Field()
  content = scrapy.Field()
  answer_num = scrapy.Field()
  comments_num = scrapy.Field()
  watch_user_num = scrapy.Field()
  click_num = scrapy.Field()
  crawl_time = scrapy.Field()

  def get_insert_sql(self):
    # 插入知乎question表的sql语句
    insert_sql = """
            insert into zhihu_question(zhihu_id, topics, url, title, content, answer_num, comments_num,
              watch_user_num, click_num, crawl_time
              )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE content=VALUES(content), answer_num=VALUES(answer_num), comments_num=VALUES(comments_num),
              watch_user_num=VALUES(watch_user_num), click_num=VALUES(click_num)
        """
    zhihu_id = self["zhihu_id"][0]
    topics = ",".join(self["topics"])
    url = self["url"][0]
    title = "".join(self["title"])
    content = "".join(self["content"])
    answer_num = cutils.extract_num("".join(self.get("answer_num", [])))
    comments_num = cutils.extract_num("".join(self.get("comments_num", [])))
    v_watch_user_num = self.get("watch_user_num", [])
    if len(v_watch_user_num) == 2:
      watch_user_num = int(v_watch_user_num[0])
      click_num = int(v_watch_user_num[1])
    else:
      watch_user_num = 0
      click_num = 0

    crawl_time = datetime.datetime.now().strftime(SQL_DATETIME_FORMAT)

    params = (zhihu_id, topics, url, title, content, answer_num, comments_num,
              watch_user_num, click_num, crawl_time)

    return insert_sql, params


# 知乎的问题回答item
class ZhihuAnswerItem(scrapy.Item):
  zhihu_id = scrapy.Field()
  url = scrapy.Field()
  question_id = scrapy.Field()
  author_id = scrapy.Field()
  content = scrapy.Field()
  parise_num = scrapy.Field()
  comments_num = scrapy.Field()
  create_time = scrapy.Field()
  update_time = scrapy.Field()
  crawl_time = scrapy.Field()

  def get_insert_sql(self):
    # 插入知乎question表的sql语句
    insert_sql = """
            insert into zhihu_answer(zhihu_id, url, question_id, author_id, content, parise_num, comments_num,
              create_time, update_time, crawl_time
              ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
              ON DUPLICATE KEY UPDATE content=VALUES(content), comments_num=VALUES(comments_num), parise_num=VALUES(parise_num),
              update_time=VALUES(update_time)
        """

    create_time = datetime.datetime.fromtimestamp(self["create_time"]).strftime(SQL_DATETIME_FORMAT)
    update_time = datetime.datetime.fromtimestamp(self["update_time"]).strftime(SQL_DATETIME_FORMAT)
    params = (
      self["zhihu_id"], self["url"], self["question_id"],
      self["author_id"], self["content"], self["parise_num"],
      self["comments_num"], create_time, update_time,
      self["crawl_time"].strftime(SQL_DATETIME_FORMAT),
    )
    return insert_sql, params


def replace_splash(value):
  return value.replace("/", "")


def handle_strip(value):
  return value.strip()


def handle_jobaddr(value):
  addr_list = value.split("\n")
  addr_list = [item.strip() for item in addr_list if item.strip() != "查看地图"]
  return "".join(addr_list)


# 拉勾网职位
class LagouJobItem(scrapy.Item):
  title = scrapy.Field()
  url = scrapy.Field()
  salary = scrapy.Field()
  job_city = scrapy.Field(
    input_processor=MapCompose(replace_splash),
  )
  work_years = scrapy.Field(
    input_processor=MapCompose(replace_splash),
  )
  degree_need = scrapy.Field(
    input_processor=MapCompose(replace_splash),
  )
  job_type = scrapy.Field()
  publish_time = scrapy.Field()
  job_advantage = scrapy.Field()
  job_desc = scrapy.Field(
    input_processor=MapCompose(handle_strip),
  )
  job_addr = scrapy.Field(
    input_processor=MapCompose(remove_tags, handle_jobaddr),
  )
  company_name = scrapy.Field(
    input_processor=MapCompose(handle_strip),
  )
  company_url = scrapy.Field()
  crawl_time = scrapy.Field()
  crawl_update_time = scrapy.Field()

  def get_insert_sql(self):
    insert_sql = """
          insert into lagou_job(title, url, salary, job_city, work_years, degree_need,
          job_type, publish_time, job_advantage, job_desc, job_addr, company_url, company_name, job_id)
          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE job_desc=VALUES(job_desc)
      """

    job_id = extract_num(self["url"])
    params = (self["title"], self["url"], self["salary"], self["job_city"], self["work_years"], self["degree_need"],
              self["job_type"], self["publish_time"], self["job_advantage"], self["job_desc"], self["job_addr"],
              self["company_url"],
              self["company_name"], job_id)
    return insert_sql, params
