from uuid import UUID
from functools import reduce

from typing import Optional

from pvm.node import Node
from pvm.transition_state import TransitionState


class Activity(Node):
    """活动节点
    """

    def __init__(self, name: str, id: UUID = None) -> None:
        super(Activity, self).__init__(name, id)
        self._executions: list = []

    def add_execution(self, execution) -> None:
        self._executions.append(execution)

    def execute(self, token) -> Optional[list]:
        logger = token.process_context.logger
        logger.info(
            "Activity {}({}) is ready to execute.".format(self._name, self._id)
        )
        if len(self._executions) > 0:

            def _default(token):
                token.current_transition.state = TransitionState.Passed

            execution = reduce(
                lambda next_, current: current(next_),
                self._executions[::-1],
                _default,
            )
            execution(token)
        else:
            token.current_transition.state = TransitionState.Passed

        logger.info(
            "Activity {}({}) finished ths executions.".format(
                self._name, self._id
            )
        )

        if token.current_transition.state == TransitionState.Passed:
            logger.info("Activity {}({}) passed.".format(self._name, self._id))
            return [t for t in self.outgoing_transitions if t.validate(token)]
        else:
            logger.info(
                "Activity {}({}) is waiting for user's feed back.".format(
                    self._name, self._id
                )
            )
            return None
