from pvm.node import Node


class StartEvent(Node):
    """流程开始事件
    """

    def __init__(self, id=None):
        super(StartEvent, self).__init__(id)

    def add_incoming_transition(self, transition):
        raise NotImplemented()

    def execute(self, token):
        token.process_context.logger.info(
            "Start Event({}) occurs.".format(self._id)
        )
        return [t for t in self.outgoing_transitions if t.validate(token)]
