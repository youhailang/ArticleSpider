workon py3.5
pip install d:\Twisted-17.9.0-cp35-cp35m-win_amd64.whl
pip install  scrapy
pip install pypiwin32 -i https://pypi.douban.com/simple/

scrapy genspider jobbole blog.jobbole.com

ROBOTSTXT_OBEY = False

调试单个url
scrapy shell http://blog.jobbole.com/113789/

pip install pillow -i https://pypi.douban.com/simple/
pip install mysqlclient -i https://pypi.douban.com/simple/

django scrapy item