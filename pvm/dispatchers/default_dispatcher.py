from pvm.walker import Walker
from pvm.transition_state import TransitionState
from pvm.token import Token


class DefaultDispatcher(object):
    """默认调度器，用于调度Walker
    """

    def __init__(self):
        self._walkers = []

    @property
    def next_walker(self):
        return next(
            (
                w
                for w in self._walkers
                if w.token.current_transition.state != TransitionState.Waiting
            ),
            None,
        )

    def create_walker(self, context, transition, token=None):
        if token is None:
            token = Token(context)

        walker = Walker()
        token.transitions.append(transition)
        walker.token = token
        self._walkers.append(walker)

    def dispatch(self, data, id=None):
        walker = None

        if id is not None:
            walker = self._find_waiting_walker(id)
        else:
            walker = self.next_walker

        if walker is not None:
            walker.token.merge(data)

        while walker:
            self._dispatch(walker)
            walker = self.next_walker

    def _dispatch(self, walker):
        transitions = walker.walk()

        if transitions:
            first = True

            for t in transitions:
                if first:
                    first = False
                    walker.token.transitions.append(t)
                else:
                    self.create_walker(
                        walker.token.process_context, t, walker.token.clone()
                    )
        elif walker.token.current_transition.state != TransitionState.Waiting:
            self._walkers.remove(walker)

    def _find_waiting_walker(self, id):
        return next(
            (
                w
                for w in self._walkers
                if w.token.current_transition.state == TransitionState.Waiting
            ),
            None,
        )
