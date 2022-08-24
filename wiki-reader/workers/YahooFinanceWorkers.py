import threading
from bs4 import BeautifulSoup
from lxml import etree #to use xpath
import requests
import time
import random

class YahooFinanceWorker(threading.Thread):

	def __init__(self, symbol, **kwargs):
		super(YahooFinanceWorker, self).__init__(**kwargs)
		self._symbol = symbol
		self._url = f"https://finance.yahoo.com/quote/{self._symbol}"
		self.start()

	def _extract_current_stock_price(self):
		r = requests.get(self._url)

		if r.status_code != 200:
			raise Exception("Unable to retrieve response from request")

		page_contents = BeautifulSoup(r.content, 'html.parser')
		dom = etree.HTML(str(page_contents))
		price = dom.xpath('//*[@id="quote-header-info"]/div[3]/div[1]/div/fin-streamer[1]')[0].text

		assert type(float(price)) == float, f"price: {price} is not a float"

	def run(self):
		time.sleep(30*random.random()) #sleep between 0 -> 20 seconds
		self._extract_current_stock_price()