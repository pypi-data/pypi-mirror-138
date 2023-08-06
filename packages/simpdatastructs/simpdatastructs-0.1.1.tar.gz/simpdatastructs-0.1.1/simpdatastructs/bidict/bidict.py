from copy import copy, deepcopy
from ..base import make_hashable, is_hashable

class bidict():

    __slots__ = ('dictionary')

    def __init__(self, **kargs):

        self.dictionary = kargs.get('dct', {})

    def __getitem__(self, key):
        return self.dictionary.__getitem__(key)
    def __setitem__(self, key, item):
        self.dictionary.__setitem__(key, item)
        self.dictionary.__setitem__(item, key)
    def __delitem__(self, key):
        self.dictionary.__delitem__(self.__getitem__(key))
        self.dictionary.__delitem__(key)
    def setdefault(self, *args, **kargs):
        if len(args) == 1:
            self.__getitem__(args[0])
        elif len(args) == 2:
            if args[0] in self.dictionary:
                return self.__getitem__(args[0])
            else:
                self.__setitem__(args[0], args[1])
                return args[1]
        else:
            raise ValueError('Expected 1-2 arguments')
    def copy(self):
        return bidict(dct=self.dictionary.copy())
    def clear(self):
        self.dictionary.clear()
    @classmethod
    def fromkeys(cls, *args, **kargs):
        raise NotImplementedError('Cannot use fromkeys on bidict')
    def get(self, *args, **kargs):
            return self.dictionary.get(*args, **kargs)
    def items(self):
        return self.dictionary.items()
    def keys(self):
        return self.dictionary.keys()
    def __pop__(self, key):
        item = self.dictionary(key)
    def pop(self, *args):
        if len(args) == 0:
            raise ValueError('Expected a key to pop')
        elif len(args) == 1 and not self.has_dflt:
            item = self.dictionary.pop(args[0])
            del self.dictionary[item]
            return item
        elif len(args) == 2 or self.has_dflt:
            try:
                item = self.dictionary.pop(args[0])
                del self.dictionary[item]
                return item
            except:
                if len(args) == 2:
                    return args[1]
                return self.dflt
    def popitem(self):
        key_item = self.dictionary.popitem()
        _ = self.dictionary.pop(key_item[1])
        return set(key_item)

    def update(self, other):
        if instance(other, bidict):
            other = other.to_dict()
        keys, items = set(), set()
        for key, item in other.items():
            keys.add(key)
            items.add(item)
            if key in item or item in key:
                if self.get(key) != item:
                    raise TypeError('Provided value violates bidict rules')
            self[key] = item
        return
    def values(self):
        return self.dictionary.values()
    def __hash__(self):
        return make_hashable(self.to_dict()).__hash__()
    def __eq__(self, other):
        if isinstance(other, bidict):
            other = other.to_dict()
        elif not isinstance(other, (bidict, dict)):
            raise TypeError('Expected bidict or dict')
        return (self.to_dict() == other)
    def to_dict(self):
        return self.dictionary
    def __str__(self):
        return self.dictionary.__str__()
    def __repr__(self):
        return self.dictionary.__repr__()




'''
clear()	Removes all items from the dictionary
copy()	Returns a shallow copy of the dictionary
fromkeys()	Creates a dictionary from the given sequence
get()	Returns the value for the given key
items()	Return the list with all dictionary keys with values
keys()	Returns a view object that displays a list of all the keys in the dictionary in order of insertion
pop()	Returns and removes the element with the given key
popitem()	Returns and removes the key-value pair from the dictionary
setdefault()	Returns the value of a key if the key is in the dictionary else inserts the key with a value to the dictionary
update()	Updates the dictionary with the elements from another dictionary
values()	Returns a list of all the values available in a given dictionary
'''
