from scrapy.selector import Selector
from selenium import webdriver
import time

from utils.common import cutils

browser = webdriver.Chrome(executable_path=cutils.chrome_driver)
browser.get("https://www.zhihu.com/signin")
browser.find_element_by_css_selector('form input[name="username"]').send_keys(cutils.zhihu_user)
browser.find_element_by_css_selector('form input[name="password"]').send_keys(cutils.zhihu_pass)
t_selector = Selector(text=browser.page_source)

"""
隐藏验证码
width:0px;height:0px;opacity:0;overflow:hidden;margin:0px;padding:0px;border:0px;
"""
captcha = t_selector.css("form div.Captcha::attr(style)").extract()[0]
if 'overflow:hidden;' not in captcha:
  print("等待验证码输入")
  time.sleep(10)
browser.find_element_by_css_selector('form button.SignFlow-submitButton').click()

# 等待 z_c0 返回
cookies = browser.get_cookies()
print("wait")
while 'z_c0' not in [cookie['name'] for cookie in cookies]:
  cookies = browser.get_cookies()
  print("*" * 30)
  time.sleep(1)
for cookie in cookies:
  print(cookie['name'], cookie['value'])

browser.quit()
