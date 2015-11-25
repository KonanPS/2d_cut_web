def cut_maps (elem_dict, PALLET_LEN):
	""" 
	generates all possible ways how to cut pallet on elements
	limitation for number of elements on a pallet is PALLET_LEN
	this limit could be counted 
	"""
	# max number of elements on a pallet
	distinct_elements_list = elem_dict.keys()

	max_num_on_pallet = int( PALLET_LEN / (min(distinct_elements_list)) )
	num_of_shortest_el = elem_dict[min(distinct_elements_list)]

	max_map_length = min( (max_num_on_pallet, num_of_shortest_el) )

	result = []

	# initial num of ways
	for e in distinct_elements_list:
		result.append((e,))

	combis_in_iteration = result[:]
	acc = set(result[:])

	while len(max(acc, key=len)) < max_map_length:
		
		new_combis = set()

		for combi in combis_in_iteration:
			for el in distinct_elements_list:

				if sum(combi) + el <= PALLET_LEN: # check limit
					temp = list(combi)
					temp.append(el)
					temp = tuple(sorted(temp))
					acc.add(temp) # set won't have same items
					new_combis.add(temp)

		combis_in_iteration = new_combis.copy()

	result = list(acc)			
	return result

def cut_maps_residues(maps, PALLET_LEN):
	"""
	takes cut maps and pallet len to finds residue for each map
	returns list of tuplse (map, residue) 
	"""

	result = []

	for cut_map in maps:
		residue = PALLET_LEN - sum(cut_map)
		result. append((cut_map, residue))

	return result

def can_apply_map(elem_dict, cut_map):
	"""
	checks if map could be applied for current elem_dict (elements and its number)
	"""
	elem_dict_copy = elem_dict.copy()

	for elem in cut_map:
		elem_dict_copy[elem] -= 1

	for num in elem_dict_copy.values():
		if num < 0:
			return False 	

	return True

def apply_map(elem_dict, cut_map):
	"""
	applies cut_map to elem_dict. Decrease element num by amount it is in map
	"""
	for elem in cut_map:
		elem_dict[elem] -= 1

	return elem_dict

def find_maps_combinations_with_min_residue(elem_dict, maps_with_residue):
	"""
	starting from each map combines it with others finds combi with min sum residue
	"""
	import copy

	maps_sorted = sorted(maps_with_residue, key=lambda x: x[1]) # sorted by residue amount

	min_residue_list = [maps_sorted[0]]

	cur_map_residue = maps_sorted[0][1]
	i = 0
	while cur_map_residue == maps_sorted[0][1]:
		i += 1
		min_residue_list.append(maps_sorted[i])
		cur_map_residue = maps_sorted[i][1] 

	residue = float('inf')

	for m in min_residue_list:

		result = [elem_dict.copy(), m]
		apply_map(result[0],result[1][0])
		result_residue = result[1][1]

		it = 0

		while sum(result[0].values()):

			min_iter_residue = float('inf')

			for m in maps_with_residue:
			
				if can_apply_map(result[0], m[0]):
					temp = copy.deepcopy(result)
					temp_combi_residue = result_residue	
					temp.append(m)
					apply_map(temp[0],m[0])
					temp_combi_residue += m[1]

				if temp_combi_residue < min_iter_residue:
					min_iter_residue = temp_combi_residue
					temp_min_result = copy.deepcopy(temp) 

			result = copy.deepcopy(temp_min_result)
			result_residue = min_iter_residue

		if result_residue <= residue:
			residue = result_residue
			best = copy.deepcopy(result)

	return best, residue

def main(elem_dict, PALLET_LEN):
	"""
	combine all func together
	"""
	import time

	start_time = time.time()

	all_possible_maps = cut_maps(elem_dict, PALLET_LEN)

	all_possible_maps_with_residues = cut_maps_residues(all_possible_maps, PALLET_LEN)

	combi_with_min_residue, combi_residue = find_maps_combinations_with_min_residue(elem_dict, all_possible_maps_with_residues)

	finish_time = time.time()

	print 'Processig time: ', finish_time - start_time

	return combi_with_min_residue, combi_residue

if __name__ == '__main__':

	test_dict = {1356:6, 1346:6, 1458:2, 1376:12, 376:2, 326:8, 637:4, 717:4, 737:6, 488:2, 687:4, 448:4, 742:2, 496:10, 456:2, 886:2}
	test_dict_short = {1356:16, 1346:3, 1458:2, 1376:12, 376:1, 326:8}

	PALLET_LEN = 6400

	test_paper = {1380:22, 1520:25, 1560:12, 1710:14, 1820:18, 1880:18, 1930:20, 2000:10, 2050:12, 2100:14, 2140:16, 2150:18, 2200:20}
	PAPER_LEN = 5600
	paper_one_of_the_answers = {
								(1820,1820,1820): 2,
								(1380,2150,1930): 3,
								(1380,2150,2050): 12,
								(1380,2100,2100): 7,
								(2200,1820,1560): 12,
								(2200,1520,1880): 8,
								(1520,1930,2150): 1,
								(1520,1930,2140): 16,
								(1710,2000,1880): 10,
								(1710,1710,2150): 2 
								}
	residue_percent = 0.401 # %

	residue = 0

	for m in paper_one_of_the_answers.keys():
		residue += (PAPER_LEN - sum(m)) * paper_one_of_the_answers[m]
	


	result, combi_residue = main(test_paper, PAPER_LEN) # [{}, ((map1), residue1), ((map2), residue2), ...]

	result_dict = {}
	for m in result[1:]:
		if m[0] in result_dict:
			result_dict[m[0]] += 1
		else:
			result_dict[m[0]] = 1

	print result_dict
	print 'Total residue: ', combi_residue
	print 'Residue percent: ', float(combi_residue) * 100 / (PAPER_LEN * sum(result_dict.values()))
	print 'Original residue percent: ', float(residue) * 100 / (sum(paper_one_of_the_answers.values() * PAPER_LEN))