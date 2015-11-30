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
    print result[6]
    print 'maps done'           
    return result

def cut_maps_residues(maps, PALLET_LEN):
    """
    takes cut maps and pallet len to finds residue for each map
    returns list of tuplse (map, residue) 
    """
    import pickle

    result = []

    for cut_map in maps:
        residue = PALLET_LEN - sum(cut_map)
        result. append((cut_map, residue))

    # pickle.dump(result, open('cut_maps_with_residues.pick', 'wb'))

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

def prepare_data_for_find(elem_dict, maps_with_residue):
    """ """
    maps_sorted = sorted(maps_with_residue, key=lambda x: x[1]) # sorted by residue amount

    min_residue_list = [maps_sorted[0]]

    cur_map_residue = maps_sorted[0][1]
    i = 0
    while cur_map_residue == maps_sorted[0][1]:
        i += 1
        min_residue_list.append(maps_sorted[i])
        cur_map_residue = maps_sorted[i][1] 

    # print 'List with min residue maps done'
    # print min_residue_list
    # l = len(min_residue_list)

    return min_residue_list

def find_maps_combinations_with_min_residue(elem_dict, all_possible_maps_with_residues, start_map, filename):
    """
    starting from each map combines it with others finds combi with min sum residue
    """
    import copy, os, time
    import pickle

    print 'Strats pid %s' % (os.getpid(),)
    # print 'Strats thread %s' % (thread.get_ident(),)
    n = time.time()

    # print start_map
    # print
    # print elem_dict

    residue = float('inf')

    result = [elem_dict.copy(), start_map]
    apply_map(result[0],result[1][0])
    result_residue = result[1][1]
    temp_combi_residue = result_residue

    # ds = time.time()
    # print 'deepcopy start'
    temp = copy.deepcopy(result)
    temp_min_result = copy.deepcopy(result)
    # de = time.time()
    # print 'deepcopy ends in ', de - ds

    # file_open_s = time.time()
    # print 'pickle read start'
    maps_with_residue = all_possible_maps_with_residues
    # file_open_e = time.time()
    # print 'pickle read finish in', file_open_e - file_open_s

    while sum(result[0].values()):

        min_iter_residue = float('inf')

        # print 'len maps_with_residue: ', len(maps_with_residue)

        # fs = time.time()
        # print 'FOR start'
        for m in maps_with_residue: # finds min residue for current tree level
            
            if can_apply_map(result[0], m[0]):
                # temp = copy.deepcopy(result)
                temp_combi_residue = result_residue 
                # temp.append(m)
                # apply_map(temp[0],m[0])
                temp_combi_residue += m[1]

                if temp_combi_residue <= min_iter_residue:
                    min_iter_residue = temp_combi_residue
                    temp_min_result = copy.deepcopy(result)
                    temp_min_result.append(m)
                    apply_map(temp_min_result[0],m[0])
                # temp_min_result = copy.deepcopy(temp) 
        # fe = time.time()
        # print 'FOR ends in ', fe - fs

        result = copy.deepcopy(temp_min_result) # one step down the tree in min residue direction
        result_residue = min_iter_residue

        # print sum(result[0].values())

        # if result_residue < residue:
        #   residue = result_residue
        #   best = copy.deepcopy(result)

    # print 'Checked %s of %s' % (_it, l)
    # print residue
    e = time.time()
    pickle.dump(result, open(filename, 'wb'))
    # print 'Finish thread %s' % (thread.get_ident(),)
    print 'Process %s finished in %s seconds' % (os.getpid(), e - n,)
    return result



def try_multiprocess(elem_dict, all_possible_maps_with_residues):
    """ """
    from multiprocessing import Process, Manager, Pool
    import pickle

    result_list = []

    def log_result(result):
        # This is called whenever foo_pool(i) returns a result.
        # result_list is modified only by the main process, not the pool workers.
        result_list.append(result)

    # manager = Manager()

    pool = Pool(processes=2)
    
    maps_with_residue = all_possible_maps_with_residues

    min_residue_list = prepare_data_for_find(elem_dict, maps_with_residue) 

    # shared_maps_with_residue = manager.list(maps_with_residue)

    filename = 0
    # result_list = []

    for m in min_residue_list:

        if can_apply_map(elem_dict, m[0]):

            filename += 1
            result = pool.apply_async(find_maps_combinations_with_min_residue, args=(elem_dict, maps_with_residue, m, str(filename)), callback=log_result)

            # r = result.get()

            # result_list.append(r)

    pool.close()
    pool.join()

            # if __name__ == '__main__':
            #     p = Process(target=find_maps_combinations_with_min_residue, args=(elem_dict, maps_with_residue, m, str(filename)))
            #     p.start()
            #     p.join()

    return result_list
        
# def try_multithread(elem_dict, maps_with_residue):
#     """ """
#     import threading

#     min_residue_list = prepare_data_for_find(elem_dict, maps_with_residue) 

#     filename = 0

#     for m in min_residue_list:
#         filename += 1
#         t = threading.Thread(target=find_maps_combinations_with_min_residue, args=(elem_dict, maps_with_residue, m, str(filename)))
#         t.start()

def main(elem_dict, PALLET_LEN):
    """
    combine all func together
    """
    import time, copy

    global global_result

    global_result = []

    start_time = time.time()

    all_possible_maps = cut_maps(elem_dict, PALLET_LEN)

    all_possible_maps_with_residues = cut_maps_residues(all_possible_maps, PALLET_LEN)

    # combi_with_min_residue, combi_residue = find_maps_combinations_with_min_residue(elem_dict, all_possible_maps_with_residues)

    best_candidates = try_multiprocess(elem_dict, all_possible_maps_with_residues)

    min_residue = float('inf')
    for candidate in best_candidates:
        
        r = 0
        for m in candidate[1:]:

            r += m[1]

        if r <= min_residue:
            min_residue = r
            best = copy.deepcopy(candidate)

    print 'Best combi: ', best
    print 'Total residue: ', min_residue

    finish_time = time.time()

    print 'Processig time: ', finish_time - start_time

    # return combi_with_min_residue, combi_residue
    return None

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
# residue_percent = 0.401 # %

# residue = 0

# for m in paper_one_of_the_answers.keys():
#   residue += (PAPER_LEN - sum(m)) * paper_one_of_the_answers[m]



    result = main(test_dict, PALLET_LEN) # [{}, ((map1), residue1), ((map2), residue2), ...]

# result_dict = {}
# for m in result[1:]:
#   if m[0] in result_dict:
#       result_dict[m[0]] += 1
#   else:
#       result_dict[m[0]] = 1

# print result_dict
# print 'Total residue: ', combi_residue
# print 'Residue percent: ', float(combi_residue) * 100 / (PAPER_LEN * sum(result_dict.values()))
# print 'Original residue percent: ', float(residue) * 100 / (sum(paper_one_of_the_answers.values() * PAPER_LEN))