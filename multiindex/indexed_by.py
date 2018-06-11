from abc import ABCMeta
from . import view


class IndexIterator(object):
    def __init__(self, index_to_iterate):
        self.iterator = iter(index_to_iterate)

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.iterator)


class IndexedBy(object):
    __metaclass__ = ABCMeta
    def insert(self, obj):
        index_val = getattr(obj, self.index_name)
        self.view.insert(index_val, obj)

    def get(self, value):
        return self.view.get(value)

    def modify(self, value, obj):
        return self.view.modify(value, getattr(obj, self.index_name), obj)

    def remove(self, value):
        return self.view.remove(value)

    def can_be_inserted(self, visitor, obj):
        return visitor.visit(self, obj)

    def can_be_modified(self, visitor, obj):
        return visitor.visit(self, obj)

    def can_be_removed(self, visitor, obj):
        return visitor.visit(self, obj)

    def __iter__(self):
        return IndexIterator(self.view)


class HashedUnique(IndexedBy):
    def __init__(self, index_name):
        self.index_name = index_name
        self.view = view.HashedUnique()


class HashedNonUnique(IndexedBy):
    def __init__(self, index_name):
        self.index_name = index_name
        self.view = view.HashedNonUnique()


class OrderedUnique(IndexedBy):
    def __init__(self, index_name):
        self.index_name = index_name
        self.view = view.OrderedUnique()
