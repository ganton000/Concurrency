from multiprocessing import Pool, cpu_count

def square(x,y):
	return x**y

#num_threads = 4
def run():
	comparison_list = [1,2,3]
	power_list = [4,5,6]

	prepared_list = []
	for i in range(len(comparison_list)):
		prepared_list.append((comparison_list[i], power_list[i]))

	print("starmapped list", prepared_list)

	#processes/cores available
	num_cpu_to_use = max(1, cpu_count() - 1)

	with Pool(num_cpu_to_use) as mp_pool:
		result = mp_pool.starmap(square, prepared_list)
		print(result)

if __name__ == "__main__":
	run()