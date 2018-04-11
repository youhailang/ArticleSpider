# -*- coding: utf-8 -*-
import re

import scrapy


class JobboleSpider(scrapy.Spider):
  name = 'jobbole'
  allowed_domains = ['blog.jobbole.com']
  start_urls = ['http://blog.jobbole.com/113789/']

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

  def parse(self, response):
    post_urls = response.css('#archive .floated-thumb .post-thumb a::attr(href)')
  # self.parse_by_xpath( response)
    pass
