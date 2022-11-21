#threading better due to network I/O hinderances
#from threading import Thread

#multiprocessing used for cpu intensive processes (no networking hinderances)
from multiprocessing import Process, Queue
from time import time


def check_value_in_list(x, j, num_of_processes, queue):
	max_num_to_check = 10**8
	lower_bnd = int((j * max_num_to_check)/num_of_processes)
	upper_bnd = int(((j + 1) * max_num_to_check)/num_of_processes)

	num_of_hits = 0
	for i in range(lower_bnd, upper_bnd):
		if i in x:
			num_of_hits += 1

	queue.put((lower_bnd, upper_bnd, num_of_hits))

#num_threads = 4
def run():
	comparison_list = [1,2,3]
	num_processes = 4
	queue = Queue()

	processes = []
	for i in range(num_processes):
		t = Process(target=check_value_in_list, args=(comparison_list, i, num_processes, queue))
		processes.append(t)

	for t in processes:
		t.start()

	for t in processes:
		t.join()

	queue.put("DONE")

	while True:
		v = queue.get()
		if v == "DONE":
			break

		lower, upper, num_of_hits = v
		print("Between", lower, "and", upper, "we have", num_of_hits, "values in the list")


if __name__ == "__main__":
	start_time = time()
	run()
	print("Script time:", time() - start_time, " seconds")
