from simpdatastructs.bidict.bidict import bidict
from simpdatastructs.base import make_hashable, is_hashable

class bidict_mult(bidict):

    def __init__(self, **kargs):
        super().__init__()
        self.track_order = kargs.get('track_order', True)
        self.last_item = None

    def __setitem__(self, key, item):

        if not is_hashable(key) or not is_hashable(item):
            raise ValueError('Both key and item must be hashable')

        self.last_item = (key, item)

        if self.track_order:
            if key in self.dictionary:
                self.dictionary.get(key).append(item)
            else:
                self.dictionary[key] = [item]
            if item in self.dictionary:
                self.dictionary.get(item).append(key)
            else:
                self.dictionary[key] = [item]
        else:
            if key in self.dictionary:
                self.dictionary.get(key).add(item)
            else:
                self.dictionary[key] = set(item)
            if item in self.dictionary:
                self.dictionary.get(item).add(key)
            else:
                self.dictionary[key] = set(key)

    def copy(self):
        return bidict_mult(dictionary=self.dictionary.copy())

    @classmethod
    def fromkeys(cls, *args, **kargs):
        raise NotImplementedError('Cannot use fromkeys on bidict')

    def items(self):
        return self.dictionary.items()

    def keys(self):
        return self.dictionary.keys()

    def pop(self, *args):
        if len(args) == 0:
            raise ValueError('Expected a key to pop')
        elif len(args) == 1 and not self.has_dflt:
            item = self.dictionary.pop(args[0])
            item.discard(key)
            if len(item) > 0:
                self[key] = item
            return item
        elif len(args) == 2 or self.has_dflt:
            try:
                item = self.dictionary.pop(args[0])
                item.discard(key)
                if len(item) > 0:
                    self[key] = item
                return item
            except:
                if len(args) == 2:
                    return args[1]
                return self.dflt

    def popitem(self):

        key_node = self.dictionary.get(self.last_item[0])
        item_node = self.dictionary.get(self.last_item[1])

        key_node.discard(self.last_item[0])
        item_node.discard(self.last_item[1])

        if len(key_node) == 0:
            self.dictionary.pop(self.last_item)

        return (self.last_item[0], nodeA)

    def __pop__(key)


    def update(self, other):
        if isinstance(other, bidict):
            other = other.to_dict()
        for key, item in other.items():
            self[key] = item


import unittest
class test_bidict(unittest.TestCase):

    def test_initialization(self):
        bdm = bidict_mult()
        self.assertIsInstance(bdm, bidict_mult)
        self.assertIsInstance(bdm, bidict_mult, \
            msg="Failed to create bidict_mult")

    def test_init_from_parent(self):
        bdm = bidict_mult(multi_bigraph=True)
        self.assertIsInstance(bdm, bidict_mult, \
            msg="Failed to create bidict_mult from bidict")

    def test_

if __name__ == '__main__':
    unittest.main()
