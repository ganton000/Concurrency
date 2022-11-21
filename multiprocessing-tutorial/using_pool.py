from multiprocessing import Pool, cpu_count
from functools import partial

def square(y, add_comp, x):
	return x**y + add_comp

#num_threads = 4
def run():
	comparison_list = [1,2,3]

	#processes/cores available
	num_cpu_to_use = max(1, cpu_count() - 1)
	print(num_cpu_to_use)
	power = 3
	add_comp = 2

	partial_function = partial(square, power, add_comp)

	with Pool(num_cpu_to_use) as mp_pool:
		result = mp_pool.map(partial_function, comparison_list)
		print(result)

if __name__ == "__main__":
	run()