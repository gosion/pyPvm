from uuid import UUID
from typing import Optional

from pvm.keyed_model import KeyedModel
from pvm.node import Node
from pvm.transition_state import TransitionState


class Transition(KeyedModel):
    """连接节点的路由，代表状态转化
    """

    def __init__(self, id: UUID = None) -> None:
        super(Transition, self).__init__(id)
        self._predicates: list = []
        self.source: Optional[Node] = None
        self.destination: Optional[Node] = None
        self.state: TransitionState = TransitionState.Pending

    def add_predicate(self, predicate) -> None:
        self._predicates.append(predicate)

    def validate(self, token) -> bool:
        predicates = self._predicates
        predicates.insert(
            0, lambda t: t.current_transition.state != TransitionState.Blocked
        )

        for p in predicates:
            if p(token) is False:
                return False

        return True


if __name__ == "__main__":
    Transition()
