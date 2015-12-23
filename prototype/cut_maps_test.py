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

def cut_maps (elem_dict, PALLET_LEN):
    """ 
    generates all possible ways how to cut pallet on elements
    limitation for number of elements on a pallet is PALLET_LEN
    this limit could be counted 
    """
    import itertools

    distinct_elements_list = elem_dict.keys()

    max_num_on_pallet = int( PALLET_LEN / (min(distinct_elements_list)) )

    maps = set()
    for map_len in range(1,max_num_on_pallet + 1):
        maps_generator = itertools.combinations_with_replacement(distinct_elements_list, map_len)
        for m in maps_generator:
            if sum(m) <= PALLET_LEN:
                m_list = list(m)
                m_list.sort()
                maps.add(tuple(m))

    print 'maps done'   
    print 'maps num: ', len(maps)  
    
    return list(maps)

if __name__ == '__main__':
    test_paper = {1380:22, 1520:25, 1560:12, 1710:14, 1820:18, 1880:18, 1930:20, 2000:10, 2050:12, 2100:14, 2140:16, 2150:18, 2200:20}
    PAPER_LEN = 5600
    test_dict = {1356:6, 1346:6, 1458:2, 1376:12, 376:2, 326:8, 637:4, 717:4, 737:6, 488:2, 687:4, 448:4, 742:2, 496:10, 456:2, 886:2}
    PALLET_LEN = 6400
    cut_maps(test_dict, PALLET_LEN)
    # print (3,3,3,1) in maps