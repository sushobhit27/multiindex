from abc import ABCMeta, abstractmethod
from collections import OrderedDict, defaultdict


class View(object, metaclass=ABCMeta):
    @abstractmethod
    def insert(self, k, v):
        pass

    @abstractmethod
    def get(self, k):
        pass

    @abstractmethod
    def modify(self, k, v):
        pass

    @abstractmethod
    def remove(self, k):
        pass


class Unique(View, metaclass=ABCMeta):
    def insert(self, k, v):
        self._container[k] = v

    def get(self, k):
        return self._container.get(k)

    def modify(self, k, v):
        self._container[k] = v

    def remove(self, k):
        del self._container[k]


class HashedUnique(Unique):
    def __init__(self):
        self._container = dict()


class OrderedUnique(Unique):
    def __init__(self):
        self._container = OrderedDict()


class HashedNonUnique(View):
    def __init__(self):
        self._container = defaultdict(list)

    def insert(self, k, v):
        self._container[k].append(v)

    def get(self, k):
        return self._container.get(k)

    def modify(self, k, v):
        if k in self._container:
            self._container[k].pop(0)
            self._container[k].append(v)

    def remove(self, k):
        if k in self._container:
            self._container[k].pop(0)