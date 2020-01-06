import uuid

from pvm.process import Process
from pvm.transition import Transition
from pvm.events.start_event import StartEvent
from pvm.events.end_event import EndEvent
from pvm.activities import ACTIVIES


class ProcessBuilder(object):
    """流程实例建造者
    """

    def __init__(self):
        self._nodes = []
        self._transitions = []
        self._start_transition = None
        self._features = {}

    def add_activity(self, name, action=None, type: str = None):
        type = type or "Activity"

        if type not in ACTIVIES:
            raise Exception("Invalid type %s" % type)

        activity = ACTIVIES[type.upper()](name)

        if action:
            action(activity)
        self._nodes.append(activity)

        return self

    def add_transition(self, source_name, destination_name):
        source = self._find_node(source_name)
        destination = self._find_node(destination_name)
        self._add_transition(source, destination)

        return self

    def add_execution(self, activity_name, execution):
        self._find_node(activity_name).add_execution(execution)

        return self

    def set_start(self, activity_name, event_name=None):
        activity = self._find_node(activity_name)

        if event_name is None:
            event_name = uuid.uuid1()

        start = self._find_node(event_name)

        if start is None:
            start = StartEvent(event_name)

        self._add_transition(start, activity)

        virtual = Transition()
        virtual.destination = start
        activity.add_incoming_transition(virtual)
        self._start_transition = virtual

        return self

    def use_feature(self, name, feature):
        self._features[name] = feature

        return self

    def build(self, dispatcher=None):
        process = Process(dispatcher)
        self._prepare_features(process)

        return self._build(process)

    def _add_transition(self, source, destination):
        transition = Transition()
        transition.source = source
        transition.destination = destination
        self._transitions.append(transition)
        source.add_outgoing_transition(transition)
        destination.add_incoming_transition(transition)

    def _find_node(self, name):
        return next((n for n in self._nodes if n.name == name), None)

    def _prepare_features(self, process):
        for k, v in self._features.items():
            process.process_context.features[k] = v

            if hasattr(v, "enable"):
                v.enable()

    def _build(self, process):
        process.dispatcher.create_walker(
            process.process_context, self._start_transition
        )
        end = None

        for node in self._nodes:
            if isinstance(node, EndEvent):
                continue

            if (node.outgoing_transitions is None) or (
                len(node.outgoing_transitions) == 0
            ):
                if end is None:
                    end = EndEvent(uuid.uuid1())

                self._add_transition(node, end)

        if end:
            self._nodes.append(end)

        return process
