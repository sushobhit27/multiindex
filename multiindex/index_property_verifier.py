from abc import abstractmethod, ABCMeta

from .indexed_by import (HashedUnique, OrderedUnique, HashedNonUnique)


class MultiIndexVisitor(object, metaclass=ABCMeta):
    @abstractmethod
    def visit(self):
        pass


class MultiIndexInserter(object):
    def visit(self, index, obj):
        index_val = getattr(obj, index.index)
        if isinstance(index, (OrderedUnique, HashedUnique)):
            # not unique, don't insert
            if index.get(index_val) is not None:
                return False
        return True


class MultiIndexModifier(object):
    def visit(self, index, obj):
        if isinstance(index, (OrderedUnique, HashedUnique)):
            # not unique, don't insert
            new_index_val = getattr(obj, index.index)
            if index.get(new_index_val):
                return False

        return True
    # def visit(self, index, indexed_by, value, obj):
    #     if index.index == indexed_by:
    #         current_index_val = index.get(value)
    #         if not current_index_val:
    #             return False
    #
    #     if isinstance(index, (OrderedUnique, HashedUnique)):
    #         # not unique, don't insert
    #         current_index_val = index.get(value)
    #         new_index_val = getattr(obj, index.index)
    #         if current_index_val == new_index_val:
    #             return False
    #
    #     return True


class MultiIndexDeleter(object):
    def visit(self, index, obj):
        index_val = getattr(obj, index.index)
        if index.get(index_val):
            return index_val
        return None