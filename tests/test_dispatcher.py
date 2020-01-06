import pytest

from pvm.dispatchers.default_dispatcher import DefaultDispatcher
from pvm.activities.activity import Activity
from pvm.transition import Transition
from pvm.delegate import delegateify
from pvm.token import Token
from pvm.transition_state import TransitionState
from pvm.process_context import ProcessContext


@delegateify
def d1(n, t):
    print("d1")
    t.current_transition.state = TransitionState.Blocked


@delegateify
def d2(n, t):
    print("d2")
    n(t)


token: Token = Token(ProcessContext())
executions = [(d1,), (d2,), (d1, d2), (d2, d1)]
expected = [
    TransitionState.Blocked,
    TransitionState.Passed,
    TransitionState.Blocked,
    TransitionState.Blocked,
]
params = zip([token] * 4, executions, expected)


@pytest.mark.parametrize("token, executions, expected", params)
def test_default_dispatcher(token, executions, expected):
    a = Activity("a")
    s = Transition("s")
    a.add_incoming_transition(s)
    s.destination = a
    for e in executions:
        a.add_execution(e)
    token.transitions.append(s)
    dispatcher = DefaultDispatcher()
    dispatcher.create_walker(token.process_context, s)
    dispatcher.dispatch({})

    assert expected == token.current_transition.state
