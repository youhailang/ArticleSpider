import hashlib
import os
import re

config = {}
with open(os.path.join(os.environ['USERPROFILE'], "ArticleSpider.txt")) as f:
  for line in f.readlines():
    ss = line.split("=", 2)
    if len(ss) == 2:
      config[ss[0].strip()] = ss[1].strip()
  f.close()
zhihu_user = config.get('zhihu.user', '')
zhihu_pass = config.get('zhihu.password', '')

def get_md5(url):
  if isinstance(url, str):
    url = url.encode("utf-8")
  m = hashlib.md5()
  m.update(url)
  return m.hexdigest()


def extract_num(text):
  # 从字符串中提取出数字
  match_re = re.match(".*?(\d+).*", text)
  if match_re:
    nums = int(match_re.group(1))
  else:
    nums = 0
  return nums


if __name__ == "__main__":
  print(config)
