# 加载cookie
import os
import pickle

from common import cutils

root_path = cutils.create_tmp_dir('zhihu')[0]
if os.path.exists(root_path):
  for filename in os.listdir(root_path):
    with open(os.path.join(os.path.join(root_path, filename)), "rb") as f:
      cookie = pickle.load(f)
      print(cookie)
