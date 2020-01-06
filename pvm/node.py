from uuid import UUID

from pvm.keyed_model import KeyedModel


class Node(KeyedModel):
    """流程节点基类
    """

    def __init__(self, name: str, id: UUID = None) -> None:
        super(Node, self).__init__(id)
        self._name: str = name
        self.incoming_transitions: list = []
        self.outgoing_transitions: list = []

    @property
    def name(self) -> str:
        return self._name

    def add_incoming_transition(self, transition) -> None:
        self.incoming_transitions.append(transition)

    def add_outgoing_transition(self, transition) -> None:
        self.outgoing_transitions.append(transition)
