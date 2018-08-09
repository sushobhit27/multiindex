import copy
import sys
import inspect

from functools import partialmethod, partial

from .index_property_verifier import (MultiIndexInserter,
                                      MultiIndexModifier,
                                      MultiIndexDeleter)
from .indexed_by import (HashedUnique,
                         HashedNonUnique,
                         OrderedUnique)


class MultiIndexContainer(object):
    def __init__(self, *indexes):
        self.indexes = {index.index_name: index for index in indexes}

        for index in self.indexes:
            setattr(self, 'get_by_' + index, partial(self.get, index))

    def insert(self, obj, overwrite=False):
        # add overwrite flag to skip index property checking.
        # although this should be handled in modify function, but for that
        # implementation will have to be changed.
        # insert must insert the obj only when every index property is satisfied.
        inserter = MultiIndexInserter()
        can_be_inserted = [index.can_be_inserted(inserter, obj, overwrite)
                           for index in self.indexes.values()]
        if all(can_be_inserted):
            for index in self.indexes.values():
                index.insert(obj)

    def get(self, indexed_by, value):
        index = self.indexes.get(indexed_by)
        return None if index is None else index.get(value)

    def modify(self, indexed_by, value, new_value):
        # modify must modify the obj only when every index property is satisfied.
        modifier = MultiIndexModifier()
        old_obj = self.get(indexed_by, value)

        if isinstance(old_obj, (list, tuple)):
            old_obj = old_obj[0]
        obj = copy.copy(old_obj)
        setattr(obj, indexed_by, new_value)
        can_be_modified = [index.can_be_modified(modifier, obj) for index in self.indexes.values()
                           if index.index_name == indexed_by]
        if all(can_be_modified):
            for index in self.indexes.values():
                index.modify(getattr(old_obj, index.index_name), obj)

    def replace(self, indexed_by, index_value, new_obj):
        modifier = MultiIndexModifier()
        can_be_modified = [index.can_be_modified(modifier, new_obj, overwrite=True)
                           for index in self.indexes.values()
                           if index.index_name == indexed_by]
        if all(can_be_modified):
            old_obj = self.get(indexed_by, index_value)
            for index in self.indexes.values():
                index.remove(getattr(old_obj, index.index_name))
                index.insert(new_obj)

    def remove(self, indexed_by, value):
        # insert must only insert the obj only when every index property is satisfied.
        index = self.indexes.get(indexed_by)
        assert index, 'Index provided does not exists in Container'
        obj = index.get(value)
        if isinstance(obj, (list, tuple)):
            obj = obj[0]

        deleter = MultiIndexDeleter()
        can_be_removed = [index.can_be_removed(deleter, obj) for index in self.indexes.values()]
        if all(can_be_removed):
            for index in self.indexes.values():
                index.remove(getattr(obj, index.index_name))

    def modify_index(self, index, value):
        raise NotImplementedError

    def get_index(self, index):
        assert index in self.indexes.keys(), 'Unknown index "{}" is provided'.format(index)
        return self.indexes[index]

    def __str__(self):
        pass

    def to_string_by(self, index):
        assert index in self.indexes.keys(), 'Unknown index "{}" is provided'.format(index)
        index_val = self.get_index(index)
        for k, v in index_val:
            print(k, v)
