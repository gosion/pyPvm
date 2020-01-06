from functools import update_wrapper


class DictProperty(object):
    """描述器，使访问属性更方便
    """

    def __init__(self, storage_name, read_only=False):
        self._storage_name = storage_name
        self._read_only = read_only

    def __call__(self, func):
        update_wrapper(self, func, updated=[])
        self._func = func
        self._name = func.__name__
        return self

    def __get__(self, instance, owner):
        if instance is None:
            return self

        storage = getattr(instance, self._storage_name)

        if storage is None:
            raise Exception("Invalid storage name")

        if self._name not in storage:
            storage[self._name] = self._func(instance)

        return storage[self._name]

    def __set__(self, instance, value):
        if self._read_only:
            raise AttributeError("Cannot set value to read-only property")

        getattr(instance, self._storage_name)[self._name] = value

    def __delete__(self, instance):
        if self._read_only:
            raise AttributeError("Cannot delete read-only property")

        del getattr(instance, self._storage_name)[self._name]
