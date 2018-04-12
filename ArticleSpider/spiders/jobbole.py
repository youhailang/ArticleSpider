# -*- coding: utf-8 -*-
import re
from urllib import parse

import scrapy
from scrapy import Request

from ArticleSpider.items import JobBoleArticleItem, ArticleItemLoader
from ArticleSpider.utils.commom import get_md5


class JobboleSpider(scrapy.Spider):
  name = 'jobbole'
  allowed_domains = ['blog.jobbole.com']
  start_urls = ['http://blog.jobbole.com/all-posts/']

  def parse_by_xpath(self, response):
    # 标题
    title = response.xpath('//div[@class="entry-header"]/h1/text()').extract()[0]
    # 创建时间
    create_date = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()').extract()[0].replace("·", "").strip()
    # 点赞
    agree = int(response.xpath('//span[contains(@class,"vote-post-up")]//h10/text()').extract()[0])
    # 收藏
    bookmark = int(
      re.match(r'.*(\d+).*', response.xpath('//span[contains(@class,"bookmark-btn")]/text()').extract()[0]).group(1))
    # 评论
    comment = int(
      re.match(r'.*(\d+).*', response.xpath('//a[@href="#article-comment"]/text()').extract()[0]).group(1))
    # 正文内容
    content = response.xpath('//div[@class="entry"]').extract()[0]
    # 标签
    tag_list = response.xpath("//p[@class='entry-meta-hide-on-mobile']/a/text()").extract()
    tag_list = [element for element in tag_list if not element.strip().endswith('评论')]
    tags = ','.join(tag_list)

  def parse_by_css(self, response):
    # 标题
    title = response.css('div.entry-header h1::text').extract()[0]
    # 创建时间
    create_date = response.css('p.entry-meta-hide-on-mobile::text').extract()[0].replace("·", "").strip()
    # 点赞
    agree = int(response.css('span.vote-post-up h10::text').extract()[0])
    # 收藏
    bookmark = int(
      re.match(r'.*(\d+).*', response.css('span.bookmark-btn::text').extract()[0]).group(1))
    # 评论
    comment = int(
      re.match(r'.*(\d+).*', response.css('a[href="#article-comment"]::text').extract()[0]).group(1))
    # 正文内容
    content = response.css('div.entry').extract()[0]
    # 标签
    tag_list = response.css('p.entry-meta-hide-on-mobile a::text').extract()
    tag_list = [element for element in tag_list if not element.strip().endswith('评论')]
    tags = ','.join(tag_list)

  def parse_detail(self, response):
    item_loader = ArticleItemLoader(item=JobBoleArticleItem(), response=response)
    # 通过item loader加载item
    front_image_url = response.meta.get("front_image_url", "")  # 文章封面图
    item_loader.add_css("title", ".entry-header h1::text")
    item_loader.add_value("url", response.url)
    item_loader.add_value("url_object_id", get_md5(response.url))
    item_loader.add_css("create_date", "p.entry-meta-hide-on-mobile::text")
    item_loader.add_value("front_image_url", [front_image_url])
    item_loader.add_css("praise_nums", ".vote-post-up h10::text")
    item_loader.add_css("comment_nums", "a[href='#article-comment'] span::text")
    item_loader.add_css("fav_nums", ".bookmark-btn::text")
    item_loader.add_css("tags", "p.entry-meta-hide-on-mobile a::text")
    item_loader.add_css("content", "div.entry")
    yield item_loader.load_item()

  def parse(self, response):
    # 文章列表
    post_nodes = response.css('#archive .floated-thumb .post-thumb a')
    for post_node in post_nodes:
      print(post_node)
      front_image_url = parse.urljoin(response.url, post_node.css('img::attr(src)').extract_first(""))
      post_url = parse.urljoin(response.url, post_node.css('::attr(href)').extract_first(""))
      yield Request(url=post_url, meta={"front_image_url": [front_image_url]}, callback=self.parse_detail)
    # 提取下一页并重新解析文章
    # next_url = response.css(".next.page-numbers::attr(href)").extract_first("")
    # if next_url:
    #   yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)
