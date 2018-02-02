def dict_to_list(dct, key_list):
    return [dct[key] for key in key_list]

def list_to_dict(L, key_list):
    return {key_list[i]: L[i] for i in range(len(L))}

def list_range_to_dict(L):
    return list_to_dict(L, range(len(L)))
