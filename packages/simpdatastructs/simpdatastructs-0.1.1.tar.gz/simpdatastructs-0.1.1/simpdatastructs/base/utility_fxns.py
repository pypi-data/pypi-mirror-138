from copy import deepcopy

def is_iter(obj):
    try:
        iter(obj)
        return True
    except:
        return False

def is_hashable(obj):
    try:
        hash(obj)
        return True
    except:
        return False

def hash_set(set_obj):
    return frozenset(set_obj)

def hash_list(lst):
    lst = deepcopy(lst)
    for indx in enumerate(lst):
        if is_hashable(item):
            continue
        else:
            lst[indx] = make_hashable(lst[indx])
    if instance(lst, list):
        return tuple(lst)
    elif isinstance(lst, tuple):
        return lst

def hash_dict(dct):
    dct = deepcopy(dct)
    # Verify hashability
    for key, item in dct.items():
        if is_hashable(item):
            continue
        else:
            dct[key] = make_hashable(item)
    # Place in tuple
    keys = sorted(dct.keys())
    return tuple([(key, dct[key]) for key in keys])

def make_hashable(obj):
    if is_hashable(obj):
        return obj
    elif isinstance(obj, set):
        return hash_set(obj)
    elif isinstance(obj, (list, tuple)):
        return hash_list(obj)
    elif isinstance(obj, (dict)):
        return hash_dict(obj, (dict))
