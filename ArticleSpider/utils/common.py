import codecs
import hashlib
import os
import re


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


# 获取知乎账号密码
def zhihu_account():
  f = codecs.open(os.path.join(os.environ['USERPROFILE'], "zhihu.txt"), 'r', encoding="utf-8")
  user = f.readline().strip()
  passwd = f.readline().strip()
  return user, passwd


if __name__ == "__main__":
  print(zhihu_account())
