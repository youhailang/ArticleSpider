from selenium import webdriver
from scrapy.selector import Selector

browser = webdriver.Chrome(executable_path="d:/chromedriver.exe")
browser.get("https://detail.tmall.com/item.htm?id=39242951579&spm=a1z09.2.0.0.b2172e8d8F7S86&_u=amedfo4380c")

# print(browser.page_source)
t_selector = Selector(text=browser.page_source)
print(t_selector.css("span.tm-price::text").extract())
browser.quit()
