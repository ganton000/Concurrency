import threading

import requests
from bs4 import BeautifulSoup

class WikiWorkerMasterScheduler(threading.Thread):

	def __init__(self, **kwargs):
		super(WikiWorkerMasterScheduler, self).__init__(**kwargs)
		self.start()

	def run(self):
		while True:
			pass


class WikiWorker():
	def __init__(self, url, **kwargs):
		self._url = url

	@staticmethod #no class properties are used (no self param)
	def _extract_company_symbols(page_html):
		soup = BeautifulSoup(page_html, features='html.parser')
		table = soup.find(id='constituents')
		table_rows = table.find_all('tr')

		#skip first row
		for table_row in table_rows[1:]:
			symbol = table_row.find('td').text.strip('\n')
			yield symbol #using generator instead of list

	def get_sp_500_companies(self):

		response = requests.get(self._url)
		if response.status_code != 200:
			print("Couldn't retrieve companies")
			return []

		yield from self._extract_company_symbols(response.text)
