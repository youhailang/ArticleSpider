import hashlib
import os
import re


class CommonUtils(object):

  def __init__(self, name='ArticleSpider.txt'):
    self.config = {}
    with open(os.path.join(os.environ['USERPROFILE'], name)) as f:
      for line in f.readlines():
        ss = line.split("=", 2)
        if len(ss) == 2:
          self.config[ss[0].strip()] = ss[1].strip()
      f.close()
    self.zhihu_user = self.config.get('zhihu.user', '')
    self.zhihu_pass = self.config.get('zhihu.password', '')
    self.chrome_driver = self.config.get('chromedriver', '')
    self.project_home = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    self.tmp_dir = self.config.get('tmpdir', os.path.join(os.environ['USERPROFILE'], "tmp"))
    self.cookie_path = self.config.get('cookie_path', os.path.join(self.tmp_dir, "cookie"))
    self.image_path = self.config.get('image_path', os.path.join(self.tmp_dir, "images"))
    # self.ua_list =

  # 创建临时文件夹并返回
  def create_tmp_dir(self, *names):
    def test_and_mkdir(p):
      if not os.path.exists(p):
        print("Create temporary direction : %s" % p)
        os.makedirs(p)
      return p

    test_and_mkdir(self.tmp_dir)
    return [test_and_mkdir(os.path.join(self.tmp_dir, name)) for name in names]

  # 获得指定url的 md5
  @staticmethod
  def get_md5(url):
    if isinstance(url, str):
      url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()

  # 从字符串中提取出数字
  @staticmethod
  def extract_num(text):
    match_re = re.match(".*?(\d+).*", text)
    if match_re:
      nums = int(match_re.group(1))
    else:
      nums = 0
    return nums

  # 使用 selenium 登录知乎并返回cookies
  def zhihu_login_sel(self, login_url, *cookie_names):
    from selenium import webdriver
    from scrapy import Selector
    import time
    browser = webdriver.Chrome(executable_path=cutils.chrome_driver)
    browser.get(login_url)
    time.sleep(1)
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
      time.sleep(10)
    else:
      browser.find_element_by_css_selector('form button.SignFlow-submitButton').click()
    # 等待 cookie_names 加载完成
    v_cookies = browser.get_cookies()
    if cookie_names:
      cookie_names_set = set(filter(lambda x: x and len(x) > 0, cookie_names))
      print("wait for cookie_names -> : " + ",".join(cookie_names_set))
      intersection_set = set([c['name'] for c in v_cookies]).intersection(cookie_names_set)
      while len(intersection_set) != len(cookie_names_set):
        print("cookie -> %s 命中(%s),剩余(%s)" % ('*' * 20, ",".join(intersection_set),
                                              ",".join(cookie_names_set - intersection_set)))
        time.sleep(1)
        v_cookies = browser.get_cookies()
        intersection_set = set([c['name'] for c in v_cookies]).intersection(cookie_names_set)
    print("cookie -> %s 命中(%s),剩余(%s)" % ('-' * 20, ",".join(intersection_set),
                                          ",".join(cookie_names_set - intersection_set)))
    browser.close()
    return v_cookies

  # 加载 知乎本地cookie
  def zhihu_load_cookies(self):
    cookies = {}
    import pickle
    root_path = cutils.create_tmp_dir('zhihu')[0]
    if os.path.exists(root_path):
      for filename in os.listdir(root_path):
        with open(os.path.join(os.path.join(root_path, filename)), "rb") as f:
          cookie = pickle.load(f)
          cookies[cookie['name']] = cookie['value']
    return cookies




cutils = CommonUtils()

if __name__ == "__main__":
  print(cutils.cookie_path)
  print(cutils.zhihu_login_sel("z_c0"))
