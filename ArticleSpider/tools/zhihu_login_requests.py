import requests

from utils.common import cutils

try:
  import cookielib
except:
  import http.cookiejar as cookielib

import re

session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename="cookies.txt")
try:
  session.cookies.load(ignore_discard=True)
except:
  print("cookie未能加载")

agent = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"
header = {
  "HOST": "www.zhihu.com",
  "Referer": "https://www.zhizhu.com",
  'User-Agent': agent
}


def is_login():
  # 通过个人中心页面返回状态码来判断是否为登录状态
  inbox_url = "https://www.zhihu.com/people/edit"
  response = session.get(inbox_url, headers=header, allow_redirects=False)
  if response.status_code != 200:
    return False
  else:
    return True


def get_xsrf():
  # 获取xsrf code
  response = session.get("https://www.zhihu.com", headers=header)
  match_obj = re.match('.*name="_xsrf" value="(.*?)"', response.text)
  if match_obj:
    return (match_obj.group(1))
  else:
    return ""


def get_index():
  response = session.get("https://www.zhihu.com", headers=header)
  with open("index_page.html", "wb") as f:
    f.write(response.text.encode("utf-8"))
  print("ok")


def get_captcha():
  import time
  t = str(int(time.time() * 1000))
  captcha_url = "https://www.zhihu.com/captcha.gif?r={0}&type=login".format(t)
  t = session.get(captcha_url, headers=header)
  with open("captcha.jpg", "wb") as f:
    f.write(t.content)
    f.close()
  from PIL import Image
  try:
    im = Image.open("captcha.jpg")
    im.show()
    im.close()
  except:
    pass
  return input("请输入验证码\n>")


def zhihu_login(account, password):
  # 知乎登录
  if re.match("^1\d{10}", account):
    print("手机号码登录")
    post_url = "https://www.zhihu.com/login/phone_num"
    post_data = {
      "_xsrf": get_xsrf(),
      "phone_num": account,
      "password": password,
      "captcha": get_captcha(),
    }
  else:
    if "@" in account:
      # 判断用户名是否为邮箱
      print("邮箱方式登录")
      post_url = "https://www.zhihu.com/login/email"
      post_data = {
        "_xsrf": get_xsrf(),
        "email": account,
        "password": password,
        "captcha": get_captcha(),
      }

  response_text = session.post(post_url, data=post_data, headers=header)
  print(response_text)
  session.cookies.save()


zhihu_login(cutils.zhihu_user, cutils.zhihu_pass)
# get_index()
print(is_login())
