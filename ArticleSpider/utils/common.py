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


cutils = CommonUtils()

if __name__ == "__main__":
  print(cutils.cookie_path)
