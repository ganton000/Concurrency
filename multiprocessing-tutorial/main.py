#from threading import Thread
from multiprocessing import Process
from time import time


def check_value_in_list(x):
	for i in range(10**8):
		i in x

#num_threads = 4
def run():
	comparison_list = [1,2,3]
	num_processes = 4

	processes = []
	for _ in range(num_processes):
		t = Process(target=check_value_in_list, args=(comparison_list,))
		processes.append(t)

	for t in processes:
		t.start()

	for t in processes:
		t.join()


if __name__ == "__main__":
	start_time = time()
	run()
	print("Script time:", time() - start_time, " seconds")
