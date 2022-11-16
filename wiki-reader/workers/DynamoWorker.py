import threading
from queue import Empty

from .utils import db

def call_clsinit(*args, **kwargs):
    cls = type(*args, **kwargs)
    cls._clsinit()
    return cls;

class DynamoMasterScheduler(threading.Thread):

	def __init__(self, input_queue, **kwargs):
		super(DynamoMasterScheduler, self).__init__(**kwargs)
		self._input_queue = input_queue
		self.start()


	def run(self):
		while True:
			try:
				val = self._input_queue.get(timeout=10)
			except Empty:
				print("Timeout reached in Dynamo Scheduler, stopping")
				break

			if val == "DONE":
				break

			symbol, price, extracted_time = val

			#create worker and insert into db
			dynamo_worker = DynamoWorker(symbol, price, extracted_time, "threading-example")
			dynamo_worker.insert_into_db()

class DynamoWorker():

	def __init__(self,  symbol, price, extracted_time, table_name="threading-example"):
		self._table_name = table_name
		self._symbol = symbol
		self._price = price
		self._extracted_time = extracted_time

		self._create_dynamo_table()

	def _create_dynamo_table(self):
		db.create_table(
			self._table_name
		)

	def insert_into_db(self):
		Item = {
			"symbol": {
				"S": self._symbol
			},
			"price": {
				"S": self._price
			},
			"extracted_time": {
				"S": self._extracted_time
			}
		}

		db.add_item(
			self._table_name,
			Item
		)

