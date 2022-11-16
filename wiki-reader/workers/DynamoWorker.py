import threading

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