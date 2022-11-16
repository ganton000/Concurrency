import threading
import time
import random
from queue import Empty

import requests
from bs4 import BeautifulSoup
from lxml import etree #to use xpath


class YahooFinancePriceScheduler(threading.Thread):
	def __init__(self, input_queue, output_queue, **kwargs):
		super(YahooFinancePriceScheduler, self).__init__(**kwargs)
		self._input_queue = input_queue
		temp_queue = output_queue
		if type(temp_queue) != list:
			temp_queue = [temp_queue]
		self._output_queue = temp_queue
		self.start()

	def run(self):
		while True:
			#blocking operation until value is returned

			try:
				val = self._input_queue.get(timeout=10)
			except Empty:
				print("Yahoo Scheduler queue is empty, stopping")
				break


			if val == 'DONE':
				for output_queue in self._output_queue:
					output_queue.put("DONE")
				break

			yahooFinanceWorker = YahooFinanceWorker(symbol=val)
			price = yahooFinanceWorker.get_stock_price()
			for output_queue in self._output_queue:
				output_values = (val, str(price), str(time.time()))
				output_queue.put(output_values)

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