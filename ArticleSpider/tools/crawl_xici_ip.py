# 请求头
import MySQLdb
import requests
from scrapy.selector import Selector


class XiciIp(object):
  def __init__(self):
    self.table = 'proxy_ip'
    self.conn = MySQLdb.connect('127.0.0.1', 'root', '123456', 'article_spider', charset="utf8", use_unicode=True)
    self.cursor = self.conn.cursor()
    self.pageSize = 100

  def crawl_ips(self):
    headers = {
      'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"
    }
    for i in range(self.pageSize):
      url = 'http://www.xicidaili.com/nn/{0}'.format(i)
      print(url)
      response = requests.get(url, headers=headers, allow_redirects=False)
      selector = Selector(text=response.text)
      all_trs = selector.css("#ip_list tr ")
      ip_list = []
      for tr in all_trs[1:]:
        speed_str = tr.css(".bar::attr(title)").extract()[0]
        if speed_str:
          speed = float(speed_str.split("秒")[0])
          all_texts = tr.css("td::text").extract()
          ip_list.append({
            'ip': all_texts[0],
            'port': all_texts[1],
            'proxy_type': all_texts[5],
            'speed': speed,
          })
      for ip_info in ip_list:
        self.cursor.execute(
          """insert into proxy_ip(ip,port,proxy_type,speed) values (%s,%s,%s,%s) ON DUPLICATE KEY UPDATE port=VALUES(port), proxy_type=VALUES(proxy_type), speed=VALUES(speed)"""
          , (ip_info['ip'], ip_info['port'], ip_info['proxy_type'], ip_info['speed']))
      if (len(ip_list)) > 0:
        self.conn.commit()

  # 判断ip代理是否可用
  def judge_ip(self, ip, port):
    http_url = "http://www.baidu.com"
    proxy_url = "http://{0}:{1}".format(ip, port)
    try:
      proxy_dict = {
        "http": proxy_url,
      }
      response = requests.get(http_url, proxies=proxy_dict)
    except Exception as e:
      print("invalid ip and port " + proxy_url)
      self.delete_ip(ip)
      return False
    else:
      code = response.status_code
      if 200 <= code < 300:
        print("effective ip")
        return True
      else:
        print("invalid ip and port " + proxy_url)
        self.delete_ip(ip)
        return False

  # 删除无效ip
  def delete_ip(self, ip):
    sql = "delete from proxy_ip where ip='{0}'".format(ip)
    print("删除无效的ip : " + sql)
    self.cursor.execute(sql)
    self.conn.commit()
    return True

  # 获取ip代理
  def get_random_ip(self):
    random_sql = """
    SELECT ip,PORT FROM proxy_ip WHERE LOWER(proxy_type) IN ('http') ORDER BY speed LIMIT 10
    """
    result = self.cursor.execute(random_sql)
    ip_list = self.cursor.fetchall()
    if len(ip_list) == 0:
      self.crawl_ips()
      return self.get_random_ip()
    for ip_info in ip_list:
      ip = ip_info[0]
      port = ip_info[1]
      if self.judge_ip(ip, port):
        return "http://{0}:{1}".format(ip, port)
    return self.get_random_ip()


if __name__ == '__main__':
  xiciip = XiciIp()
  print(xiciip.get_random_ip())
