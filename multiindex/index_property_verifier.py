from abc import abstractmethod, ABCMeta

from .indexed_by import (HashedUnique, OrderedUnique, HashedNonUnique)


class MultiIndexVisitor(object):
    __metaclass__ = ABCMeta
    @abstractmethod
    def visit(self):
        pass


class MultiIndexInserter(object):
    def visit(self, index, obj, overwrite):
        index_val = getattr(obj, index.index_name)
        if isinstance(index, (OrderedUnique, HashedUnique)):
            # don't check if overwrite
            if overwrite:
                return True
            # not unique, don't insert
            if index.get(index_val) is not None:
                return False
        return True


class MultiIndexModifier(object):
    def visit(self, index, obj, overwrite):
        if isinstance(index, (OrderedUnique, HashedUnique)):
            # don't check if overwrite
            if overwrite:
                return True
            # not unique, don't insert
            new_index_val = getattr(obj, index.index_name)
            if index.get(new_index_val):
                return False
        return True


class MultiIndexDeleter(object):
    def visit(self, index, obj):
        index_val = getattr(obj, index.index_name)
        if index.get(index_val):
            return index_val
        return None
