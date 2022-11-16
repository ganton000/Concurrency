import threading

from ..utils import db

class DynamoMasterScheduler(threading.Thread):

	def __init__(self, input_queue, **kwargs):
		super(DynamoMasterScheduler, self).__init__(**kwargs)
		self._input_queue = input_queue
		self.start()


	def run(self):
		while True:
			val = self._input_queue.get()
			if val == "DONE":
				break

class DynamoWorker():

	def __init__(self, symbol, price, extracted_time):
		self._table_name = "demo-worker-table"
		self._symbol = symbol
		self._price = price
		self._extracted_time = extracted_time

	def _create_db_table(self):
		db.create_table(
			self._table_name
		)

	def insert_into_db(self):
		Item = {
			"symbol": {
				"S": self._symbol
			},
			"price": {
				"N": self._price
			},
			"extracted_time": {
				"N": self._extracted_time
			}
		}

		db.add_item(
			self._table_name,
			Item
		)

