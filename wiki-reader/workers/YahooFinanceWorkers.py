import threading
from bs4 import BeautifulSoup
from lxml import etree #to use xpath
import requests
import time
import random


class YahooFinancePriceScheduler(threading.Thread):
	def __init__(self, input_queue, output_queue, **kwargs):
		super(YahooFinancePriceScheduler, self).__init__(**kwargs)
		self._input_queue = input_queue
		self._output_queue = output_queue
		self.start()

	def run(self):
		while True:
			#blocking operation until value is returned
			val = self._input_queue.get()
			if val == 'DONE':
				if self._output_queue is not None:
					self._output_queue.put("DONE")
				break

			yahooFinanceWorker = YahooFinanceWorker(symbol=val)
			price = yahooFinanceWorker.get_stock_price()
			if self._output_queue is not None:
				output_values = (val, price, str(time.time()))
				self._output_queue.put(output_values)

			#print(price)
			time.sleep(random.random()) #0-1 second sleep


class YahooFinanceWorker():

	def __init__(self, symbol, **kwargs):
		super(YahooFinanceWorker, self).__init__(**kwargs)
		self._symbol = symbol
		self._url = f"https://finance.yahoo.com/quote/{self._symbol}"

	def get_stock_price(self):

		r = requests.get(self._url)

		if r.status_code != 200:
			raise Exception("Unable to retrieve response from request")

		page_contents = BeautifulSoup(r.content, 'html.parser')
		dom = etree.HTML(str(page_contents))
		price = dom.xpath('//*[@id="quote-header-info"]/div[3]/div[1]/div/fin-streamer[1]')[0].text

		price = float(price.replace(",",""))
		return price