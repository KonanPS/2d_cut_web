def can_apply_map(elem_dict, cut_map):
    """
    checks if map could be applied for current elem_dict (elements and its number)
    """
    import copy
    elem_dict_copy = copy.deepcopy(elem_dict)

    for elem in cut_map:
        elem_dict_copy[elem] -= 1

    if min( elem_dict_copy.values() ) < 0:
        return False

    # for num in elem_dict_copy.values():
    #     if num < 0:
    #         return False    

    return True

def apply_map(elem_dict, cut_map):
    """
    applies cut_map to elem_dict. Decrease element num by amount it is in map
    """
    for elem in cut_map:
        elem_dict[elem] -= 1

    return elem_dict

def how_many_times_can_apply(elem_dict, cut_map):
    """ count how many times map can be applied"""
    import copy

    temp_elem_dict = copy.deepcopy(elem_dict)
    
    n = 0

    while can_apply_map(temp_elem_dict, cut_map):
        n += 1
        apply_map(temp_elem_dict, cut_map)

    return n

if __name__ == '__main__':
	d = {1: 10, 2: 5, 3: 8}
	m1 = (1,)
	m2 = (2,)
	m3 = (3,)
	m4 = (1,2,)
	m5 = (1,2,3)

	print how_many_times_can_apply(d, m1) == 10
	print how_many_times_can_apply(d, m2) == 5
	print how_many_times_can_apply(d, m3) == 8
	print how_many_times_can_apply(d, m4) == 5
	print how_many_times_can_apply(d, m5) == 5