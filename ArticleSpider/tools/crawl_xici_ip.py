# 请求头
import MySQLdb
import requests
from scrapy.selector import Selector


def crawl_ips():
  headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"
  }
  conn = MySQLdb.connect('127.0.0.1', 'root', '123456', 'article_spider', charset="utf8", use_unicode=True)
  cursor = conn.cursor()
  for i in range(100):
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
      cursor.execute(
        """insert into proxy_ip(ip,port,proxy_type,speed) values (%s,%s,%s,%s) ON DUPLICATE KEY UPDATE port=VALUES(port), proxy_type=VALUES(proxy_type), speed=VALUES(speed)"""
        , (ip_info['ip'], ip_info['port'], ip_info['proxy_type'], ip_info['speed']))
    if (len(ip_list)) > 0:
      conn.commit()
  conn.close()


crawl_ips()
