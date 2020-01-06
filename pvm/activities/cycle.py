from uuid import UUID

from pvm.activities.activity import Activity
from pvm.transition import Transition


class Cycle(Activity):
    """自循环活动节点
    """

    def __init__(self, name: str, id: UUID = None):
        super(Cycle, self).__init__(name, id)
        self._reserved_transition = Transition()
        self._reserved_transition.source = self
        self._reserved_transition.destination = self
        self.add_incoming_transition(self._reserved_transition)
        super(Cycle, self).add_outgoing_transition(self._reserved_transition)
        self._reserved_predicate = None

    def set_predicate(self, predicate):
        """设置自循环出口条件
        """

        self._reserved_predicate = predicate
        self._reserved_transition.add_predicate(predicate)

    def add_outgoing_transition(self, transition):
        transition.add_predicate(lambda t: not self._reserved_predicate(t))
        super(Cycle, self).add_outgoing_transition(transition)
