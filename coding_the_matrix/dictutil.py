def dict2list(dct, key_list):
    return [dct[key] for key in key_list]

def list2dict(L, key_list):
    return {key_list[i]: L[i] for i in range(len(L))}

def list_range2dict(L):
    return list_to_dict(L, range(len(L)))
