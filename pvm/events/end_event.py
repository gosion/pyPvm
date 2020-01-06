from pvm.node import Node


class EndEvent(Node):
    """流程结束事件
    """

    def __init__(self, id=None):
        super(EndEvent, self).__init__(id)

    def add_outgoing_transition(self, transition) -> None:
        raise NotImplemented()

    def execute(self, token):
        token.process_context.logger.info(
            "End Event({}) occurs.".format(self._id)
        )
        return [t for t in self.outgoing_transitions if t.validate(token)]
