# 测试是否登录
import requests

from common import cutils


def is_login():
  # 请求头
  headers = {
    "HOST": "www.zhihu.com",
    "Referer": "https://www.zhizhu.com",
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"
  }

  cookies = cutils.zhihu_load_cookies()
  url = 'https://www.zhihu.com/api/v4/questions/269086788'
  response = requests.get(url, headers=headers, allow_redirects=False, cookies=cookies)
  if response.status_code != 200:
    return False
  else:
    return True


if __name__ == '__main__':
  print(is_login())
