from pvm.keyed_model import KeyedModel
from pvm.dispatchers.default_dispatcher import DefaultDispatcher
from pvm.process_context import ProcessContext


class Process(KeyedModel):
    """流程实例
    """

    def __init__(self, id=None, dispatcher=None):
        super(Process, self).__init__(id)
        self._dispatcher = dispatcher or DefaultDispatcher()
        self._process_context = ProcessContext()

    @property
    def dispatcher(self):
        return self._dispatcher

    @property
    def process_context(self):
        return self._process_context

    def start(self, data):
        """发起流程"""
        self._proceed(data)

    def proceed(self, id, data):
        """继续执行流程"""
        self._proceed(data, id)

    def _proceed(self, data, id=None):
        self._dispatcher.dispatch(data, id)
