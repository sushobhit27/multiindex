import copy

from .index_property_verifier import (MultiIndexInserter,
                                      MultiIndexModifier,
                                      MultiIndexDeleter)
from .indexed_by import (HashedUnique,
                         HashedNonUnique,
                         OrderedUnique)


class MultiIndexContainer(object):
    def __init__(self, *indexes):
        self.indexes = {index.index_name: index for index in indexes}

    def insert(self, obj):
        # insert must insert the obj only when every index property is satisfied.
        inserter = MultiIndexInserter()
        can_be_inserted = [index.can_be_inserted(inserter, obj) for index in self.indexes.values()]
        if all(can_be_inserted):
            [index.insert(obj) for index in self.indexes.values()]

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
            [index.modify(getattr(old_obj, index.index_name), obj)
             for index in self.indexes.values()]

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
            [index.remove(getattr(obj, index.index_name)) for index in self.indexes.values()]

    def modify_index(self, index, value):
        raise NotImplementedError

    def get_index(self, index):
        raise NotImplementedError

    def __str__(self):
        pass
