from copy import deepcopy

from typing import List, Optional

from pvm.utils import DictProperty as dp
from pvm.transition import Transition
from pvm.node import Node


class Token(object):
    """参与流程状态转移的必要数据
    """

    def __init__(self, process_context, environ=None):
        self.process_context = process_context
        self.environ: object = environ or {}
        self.storage: object = {}

    @dp("storage", read_only=True)
    def transitions(self) -> List[Transition]:
        return []

    def clone(self):
        return Token(self.process_context, deepcopy(self.environ))

    @property
    def current_transition(self) -> Optional[Transition]:
        if self.transitions:
            return self.transitions[-1]
        else:
            return None

    @property
    def source(self) -> Optional[Node]:
        return (
            self.current_transition.source if self.current_transition else None
        )

    @property
    def destination(self) -> Optional[Node]:
        return (
            self.current_transition.destination
            if self.current_transition
            else None
        )

    def merge(self, data):
        self.environ.update(data)
