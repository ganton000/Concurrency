from multiprocessing import Pool, cpu_count

def check_num_values_in_range(comparison_list, lower, upper):
	num_of_hits = 0
	for i in range(lower, upper):
		if i in comparison_list:
			num_of_hits += 1

	return num_of_hits

def run():
	comparison_list = [1,2,3]
	lower_and_upper_bounds = [(0, 25*10**6), (25*10**6, 50*10**6), (50*10**6, 75*10**6), (75*10**6, 100*10**6)]

	prepared_list = []
	for i in range(len(lower_and_upper_bounds)):
		prepared_list.append((comparison_list, lower_and_upper_bounds[i][0], lower_and_upper_bounds[i][1]))

	print("starmapped list", prepared_list)

	#processes/cores available
	num_cpu_to_use = max(1, cpu_count() - 1)

	with Pool(num_cpu_to_use) as mp_pool:
		result = mp_pool.starmap(check_num_values_in_range, prepared_list)
		print(result)

if __name__ == "__main__":
	run()