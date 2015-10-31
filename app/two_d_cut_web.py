
def get_data_from_file(filename, separator):
	"""
	opens file with pieces in format
	length; number

	append to pieces_list max num of element that could be placed on one pallet

	returns list with all elements
	"""	
	elements = open(filename)

	pieces_list = []
	pieces_dict = {}

	PALLET_LEN = int(elements.readline()) #first line is pallet length

	line = elements.readline()
	while line:
		temp = line.split(separator)
		length = int(temp[0])
		num = int(temp[1])
		pieces_dict[length] = num

		#pieces list is list of max int number of element on one PALLET
		for _ind in range(int(PALLET_LEN / length)):
			pieces_list.append(length)

		line = elements.readline()

	elements.close()

	return pieces_list, pieces_dict, PALLET_LEN

def gen_pallets(pieces, recur):
	"""
	takes list of all pieces and
	generates all possible combinations of different length
	returns list of conbis (list)
	"""
	import datetime
	import gc
	import sys

	recur += 1
	first = pieces[0]
	rest = pieces[1:]

	if rest:
		acc = gen_pallets(rest,recur)
	else:
		s = set()
		s.add((first,))
		return s

	new_acc = acc.copy()
	new_acc.add((first,))

	print datetime.datetime.now(), '#', recur, 'len acc:', len(new_acc), 'size', sys.getsizeof(new_acc)

	for pallet in acc:
		sum_pallet = sum(pallet)
		if sum_pallet + first <= PALLET_LEN:
			# for i in range(len(pallet) + 1):
			# 	temp = list(pallet)
			# 	temp.insert(i,first)
			# #too expensive operation	#if temp not in new_acc: #filter same pallets because of same elements
			# 	new_acc.add(tuple(temp))
			temp = list(pallet)
			temp.append(first)
			temp.sort()
			new_acc.add(tuple(temp))


	gc.collect()
	return new_acc

def delete_same_combis(combis):
	"""
	takes list of combis and delete the same 
	same are in combis because many elemets of the same length
	returns list of distinct combis
	"""
	acc = []
	
	temp = combis.pop(0)
	while temp:
		if temp not in combis:
			acc.append(temp)

		if combis:
			temp = combis.pop(0)
		else:
			break

	return acc

def delete_short_cuts(combis, MAX_ELEMENT_LENGTH):
	"""
	deletes combi that has residues more than max length of element
	"""
	acc = []
	for combi in combis:
		if (PALLET_LEN - sum(combi)) <= MAX_ELEMENT_LENGTH:
			acc.append(combi)

	combis = acc

	return combis

def first_way(pieces_dict, distinc_combis_sorted):
	"""
	takes pieces dict and distinc combis sorted by residue.
	takes first distinc combi(min residue) 
	and checks if there enough elements to apply it.
	if there is applies it and tries to use it one again (min residue)
	if not takes next combi.
	continues until there no more elements in dict.
	returns list of best cuts.

	good for small num of elements. Too slow for big amount of small elements.
	"""

	temp_pieces_dict = pieces_dict.copy()
	i = 0
	total_residue = 0
	cuts =[]
	while sum(temp_pieces_dict.values()):
		
		combi_can_be_cut = True

		elem_to_cut = {}
		for elem in distinc_combis_sorted[i]:
			if elem in elem_to_cut:
				elem_to_cut[elem] += 1
			else:
				elem_to_cut[elem] = 1

		for key, val in elem_to_cut.items():
			if temp_pieces_dict[key] >= val:
				continue
			else:
				combi_can_be_cut = False
				break

		if combi_can_be_cut:
			residue = PALLET_LEN - sum(distinc_combis_sorted[i])
			cuts.append(distinc_combis_sorted[i])
			# print i, distinc_combis_sorted[i], 'residue=', residue
			total_residue += residue
			for key, val in elem_to_cut.items():
				temp_pieces_dict[key] -= val

		else: #try the same combi because it has min residue
			i += 1 

	# print total_residue
	return cuts, total_residue

def second_way(pieces_dict):
	"""
	takes pieces dict. generates combis on dict keys (distinct elements).
	sort this distinct combis by residue. applies first one. decrease elements num in dict. try to apply one more time
	takes keys that has not zero values, gen combis, sort by residue, applly first.
	returns list of best cuts

	bad way :-(
	"""
	temp_pieces_dict = pieces_dict.copy()
	total_residue = 0
	cuts =[]

	while sum(temp_pieces_dict.values()):

		pieces = [x for x in temp_pieces_dict.keys() if temp_pieces_dict[x] != 0]
		combis = gen_pallets(pieces, 0)
		distinc_combis = delete_same_combis(combis)

		distinc_combis_sorted = sorted(distinc_combis, key=lambda pallet: PALLET_LEN - sum(pallet))

		combi_can_be_cut = True

		elem_to_cut = {}
		for elem in distinc_combis_sorted[0]:
			if elem in elem_to_cut:
				elem_to_cut[elem] += 1
			else:
				elem_to_cut[elem] = 1

		for key, val in elem_to_cut.items():
			if temp_pieces_dict[key] >= val:
				continue
			else:
				combi_can_be_cut = False
				break

		if combi_can_be_cut:
			residue = PALLET_LEN - sum(distinc_combis_sorted[0])
			cuts.append(distinc_combis_sorted[0])
			# print i, distinc_combis_sorted[i], 'residue=', residue
			total_residue += residue
			for key, val in elem_to_cut.items():
				temp_pieces_dict[key] -= val

	return cuts, total_residue

def main(**kwargs):

	global PALLET_LEN
	pieces_list = []
	pieces_dict = {}

	filename = kwargs.get('filename', None)
	data_str = kwargs.get('data_str', None)

	if filename:
		print 'debug filename', filename
		elem, pieces_dict, PALLET_LEN = get_data_from_file(filename,';') # elem, pieces_dict and PALLET_LEN
	elif data_str:
		#not DRY. copy from get_data_from_file
		print 'debug', data_str
		data = data_str.split()
		print 'debug', data
		PALLET_LEN = int(data[0])
		
		for line in data[1:]:
			temp = line.split(';')
			length = int(temp[0])
			num = int(temp[1])
			pieces_dict[length] = num

			#pieces list is list of max int number of element on one PALLET
			# for _ind in range(int(PALLET_LEN / length)):
			# 	pieces_list.append(length)

		print 'debug pieces_list', pieces_list

	# else:
	# 	print 'debug else'
	# 	pieces_dict = pieces
	# 	PALLET_LEN = LEN
	# 	print "PALLET_LEN", PALLET_LEN
	# 	elem = []
	# 	for length in pieces_dict.keys():
	# 		for _ind in range(int(PALLET_LEN / length)):
	# 			elem.append(length) 
	
	#sum_length = sum(elem)

	sum_length = 0
	elem = []
	for length, num in pieces_dict.items():
		sum_length += length * num
		for _ind in range(num):
			elem.append(length)

	
	MAX_PALLEN_NUM = int(sum_length / PALLET_LEN) + 1
	MAX_ELEMENT_LENGTH = max(elem)

	print "PALLET_LEN:", PALLET_LEN
	print "All elements:", elem
	print "MAX_ELEMENT_LENGTH:", MAX_ELEMENT_LENGTH
	print "pieces_dict:", pieces_dict
	print 'Total length: ', sum_length

	print 'Step 1. gen_pallets...starts'
	allcombis = gen_pallets(sorted(elem,reverse=True), 0)
	# min_piece = min(pieces_dict.keys())
	# max_num = int(PALLET_LEN / min_piece)
	# allcombis_generator = itertools.permutations(elem, max_num)

	print 'Step 1. gen_pallets...Done'
	
	# print 'Step 2. distinc_combis...starts'
	# distinc_combis = delete_same_combis(allcombis)
	# print 'Step 2. distinc_combis...Done'
	# print "Len:", len(distinc_combis)
	# print '-'*40

	# print 'Step 2.1 delete_short_cuts...starts'
	# distinc_combis = delete_short_cuts(distinc_combis, MAX_ELEMENT_LENGTH)
	# print 'Step 2.1 delete_short_cuts...Done'
	# print "Len:", len(distinc_combis)

	print 'Step 3. geting cuts.... starts'

	distinc_combis = []
	i = 0
	for pal in allcombis:
		distinc_combis.append(list(pal))

	print 'Step 3.1 distinc_combis_sorted'
	distinc_combis_sorted = sorted(distinc_combis, key=lambda pallet: PALLET_LEN - sum(pallet))

	print 'Step 3.2 first_way'
	cuts, total_residue = first_way(pieces_dict, distinc_combis_sorted)
	# cuts, total_residue = second_way(pieces_dict)

	print 'Step 3.3 output'
	output = open('out.txt','w')
	for cut in cuts:
		output.write(str(cut) + '\n')
	output.write('Total residue:' + str(total_residue))
	output.close()
	return cuts, total_residue

#if __name__ == '__main__':
#	main(data_str='6500\r\n123;4\r\n12345;67\r\n332;8')
#FIXME delete pallets with the same num of elements



