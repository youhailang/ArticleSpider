import datetime
import json
import os
import re

from scrapy import Selector

from items import ZhihuQuestionItem, ZhihuAnswerItem

try:
  import urlparse as parse
except:
  from urllib import parse
import scrapy
from scrapy.loader import ItemLoader
from utils.common import cutils


class ZhihuSelSpider(scrapy.Spider):
  name = "zhihu_sel"
  allowed_domains = ["www.zhihu.com"]
  start_urls = ['https://www.zhihu.com/']

  # question的第一页answer的请求url
  start_answer_url = "https://www.zhihu.com/api/v4/questions/{0}/answers?sort_by=default&include=data%5B%2A%5D.is_normal%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccollapsed_counts%2Creviewing_comments_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Cmark_infos%2Ccreated_time%2Cupdated_time%2Crelationship.is_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B%2A%5D.author.is_blocking%2Cis_blocked%2Cis_followed%2Cvoteup_count%2Cmessage_thread_token%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&offset={1}&limit={2}"

  # 请求头
  headers = {
    "HOST": "www.zhihu.com",
    "Referer": "https://www.zhizhu.com",
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"
  }

  def parse(self, response):
    """
    提取出html页面中的所有url 并跟踪这些url进行一步爬取
    如果提取的url中格式为 /question/xxx 就下载之后直接进入解析函数
    """
    all_urls = response.css("a::attr(href)").extract()
    all_urls = filter(lambda x: x.startswith("https"), [parse.urljoin(response.url, url) for url in all_urls])
    for url in all_urls:
      match_obj = re.match("(.*zhihu.com/question/(\d+))(/|$).*", url)
      if match_obj:
        # 如果提取到question相关的页面则下载后交由提取函数进行提取
        question_url = match_obj.group(1)
        yield scrapy.Request(question_url, headers=self.headers, callback=self.parse_question)
        answer_url = self.start_answer_url.format(match_obj.group(2), 0, 20)
        yield scrapy.Request(answer_url, headers=self.headers, callback=self.parse_answer)
      else:
        # 如果不是question页面则直接进一步跟踪 深度搜索
        yield scrapy.Request(url, headers=self.headers, callback=self.parse)

  def parse_question(self, response):
    # 处理question页面， 从页面中提取出具体的question item
    question_id = int(re.match("(.*zhihu.com/question/(\d+))(/|$).*", response.url).group(2))
    if "QuestionHeader-title" in response.text:
      item_loader = ItemLoader(item=ZhihuQuestionItem(), response=response)
      item_loader.add_css("title", "h1.QuestionHeader-title::text")
      item_loader.add_css("content", ".QuestionHeader-detail")
      item_loader.add_value("url", response.url)
      item_loader.add_value("zhihu_id", question_id)
      item_loader.add_css("answer_num", ".List-headerText span::text")
      item_loader.add_css("comments_num", ".QuestionHeader-actions button::text")
      item_loader.add_css("watch_user_num", ".NumberBoard-value::text")
      item_loader.add_css("topics", ".QuestionHeader-topics .Popover div::text")

      question_item = item_loader.load_item()
    else:
      # 处理老版本页面的item提取
      item_loader = ItemLoader(item=ZhihuQuestionItem(), response=response)
      # item_loader.add_css("title", ".zh-question-title h2 a::text")
      item_loader.add_xpath("title",
                            "//*[@id='zh-question-title']/h2/a/text()|//*[@id='zh-question-title']/h2/span/text()")
      item_loader.add_css("content", "#zh-question-detail")
      item_loader.add_value("url", response.url)
      item_loader.add_value("zhihu_id", question_id)
      item_loader.add_css("answer_num", "#zh-question-answer-num::text")
      item_loader.add_css("comments_num", "#zh-question-meta-wrap a[name='addcomment']::text")
      # item_loader.add_css("watch_user_num", "#zh-question-side-header-wrap::text")
      item_loader.add_xpath("watch_user_num",
                            "//*[@id='zh-question-side-header-wrap']/text()|//*[@class='zh-question-followers-sidebar']/div/a/strong/text()")
      item_loader.add_css("topics", ".zm-tag-editor-labels a::text")

      question_item = item_loader.load_item()
    yield question_item

  def parse_answer(self, response):
    # 处理question的answer
    ans_json = json.loads(response.text)
    is_end = ans_json["paging"]["is_end"]
    next_url = ans_json["paging"]["next"]

    # 提取answer的具体字段
    for answer in ans_json["data"]:
      answer_item = ZhihuAnswerItem()
      answer_item["zhihu_id"] = answer["id"]
      answer_item["url"] = answer["url"]
      answer_item["question_id"] = answer["question"]["id"]
      answer_item["author_id"] = answer["author"]["id"] if "id" in answer["author"] else None
      answer_item["content"] = answer["content"] if "content" in answer else None
      answer_item["parise_num"] = answer["voteup_count"]
      answer_item["comments_num"] = answer["comment_count"]
      answer_item["create_time"] = answer["created_time"]
      answer_item["update_time"] = answer["updated_time"]
      answer_item["crawl_time"] = datetime.datetime.now()

      yield answer_item

    if not is_end:
      yield scrapy.Request(next_url, headers=self.headers, callback=self.parse_answer)

  def start_requests(self):
    from selenium import webdriver
    browser = webdriver.Chrome(executable_path=cutils.chrome_driver)
    browser.get("https://www.zhihu.com/signin")
    browser.find_element_by_css_selector('form input[name="username"]').send_keys(cutils.zhihu_user)
    browser.find_element_by_css_selector('form input[name="password"]').send_keys(cutils.zhihu_pass)
    t_selector = Selector(text=browser.page_source)
    """
    隐藏验证码
    width:0px;height:0px;opacity:0;overflow:hidden;margin:0px;padding:0px;border:0px;
    """
    captcha_style = t_selector.css("form div.Captcha::attr(style)").extract()[0]
    if 'overflow:hidden;' not in captcha_style:
      print("10s -> 请输入验证码并提交")
      import time
      time.sleep(10)
    else:
      browser.find_element_by_css_selector('form button.SignFlow-submitButton').click()

    # 等待 z_c0 字段 调用api的时候会用到
    v_cookies = browser.get_cookies()
    print("wait for z_c0")
    while 'z_c0' not in [c['name'] for c in v_cookies]:
      v_cookies = browser.get_cookies()
      print("*" * 30)
      import time
      time.sleep(1)

    cookies = {}
    import pickle
    for cookie in v_cookies:
      with open(os.path.join(cutils.create_tmp_dir('zhihu')[0], cookie['name']), "wb") as f:
        print(cookie['name'], cookie['value'])
        pickle.dump(cookie, f)
        cookies[cookie['name']] = cookie['value']
    browser.close()
    for url in self.start_urls:
      yield scrapy.Request(url, dont_filter=True, cookies=cookies, headers=self.headers, callback=self.parse)
