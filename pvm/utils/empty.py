class EmptyCallable(object):
    """可执行对象，不做任何事情
    """

    def __get__(self, instance, owner=None):
        return self

    def __call__(self, *args, **kwargs):
        pass


class Empty(object):
    """空对象，当对象为null时，用此对象避免出现属性访问时的错误
    """

    _instance = EmptyCallable()

    def __getattr__(self, name):
        return object.__getattribute__(self, "_instance")

    def __setattr__(self, name, value):
        pass
