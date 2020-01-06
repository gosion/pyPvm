from pvm.utils import Empty


class ProcessContext(object):
    """用于存储流程实例上下文数据的对象
    """

    def __init__(self):
        self._features = {}
        self._scope = {}

    @property
    def features(self):
        """功能"""
        return self._features

    @property
    def scope(self):
        """数据"""
        return self._scope

    def __getattr__(self, name):
        if name in ("features", "scope",):
            return object.__getattribute__(self, name)
        elif name in self._features:
            return self._features[name]
        else:
            return Empty()
