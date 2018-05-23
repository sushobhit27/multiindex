from .index_property_verifier import (MultiIndexInserter,
                                      MultiIndexModifier,
                                      MultiIndexDeleter)
from .indexed_by import (HashedUnique,
                         HashedNonUnique,
                         OrderedUnique)


class MultiIndexContainer(object):
    def __init__(self, *indexes):
        self.indexes = {index_obj.index: index_obj for index_obj in indexes}

    def insert(self, obj):
        # insert must insert the obj only when every index property is satisfied.
        inserter = MultiIndexInserter()
        can_be_inserted = [index.can_be_inserted(inserter, obj) for index in self.indexes.values()]
        if all(can_be_inserted):
            [index.insert(obj) for index in self.indexes.values()]

    def get(self, index, value):
        index = self.indexes.get(index)
        return None if index is None else index.get(value)

    def modify(self, indexed_by, value, new_value):
        # modify must modify the obj only when every index property is satisfied.
        modifier = MultiIndexModifier()

        old_obj = self.get(indexed_by, value)

        if isinstance(old_obj, (list, tuple)):
            old_obj = old_obj[0]
        obj = old_obj
        setattr(obj, indexed_by, new_value)
        can_be_modified = [index.can_be_modified(modifier, obj) for index in self.indexes.values()
                           if index.index == indexed_by]
        if all(can_be_modified):
            [index.modify(getattr(old_obj, index.index), obj) for index in self.indexes.values()]

    def remove(self, indexed_by, value):
        # insert must only insert the obj only when every index property is satisfied.
        index = [index for index in self.indexes.values() if index.index == indexed_by]
        assert index, 'Index provided does not exists in Container'
        index = index[0]
        obj = index.get(value)
        if isinstance(obj, (list, tuple)):
            obj = obj[0]

        deleter = MultiIndexDeleter()
        can_be_removed = [index.can_be_removed(deleter, obj) for index in self.indexes.values()]
        if all(can_be_removed):
            [index.remove(getattr(obj, index.index)) for index in self.indexes.values()]

    def modify_index(self, index, value):
        raise NotImplementedError

    def get_index(self, index):
        raise NotImplementedError

    def __str__(self):
        pass
