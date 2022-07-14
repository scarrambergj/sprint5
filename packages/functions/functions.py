def find_in_dict(dict1, dict2, elem):
    found_elem = dict1[elem]
    return dict2.get(found_elem)