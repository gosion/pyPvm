from pvm import ProcessBuilder, delegateify
from pvm.transition_state import TransitionState
from pvm.features.logging import LogFeature, StreamWriter


@delegateify
def a2(next_, token):
    print("a2")
    input = token.environ.get("user_input", 0)
    logger = token.process_context.logger
    if input == 0:
        token.current_transition.state = TransitionState.Waiting
        logger.info("I am waiting.")
        waiting_ids = token.process_context.scope.get("waiting_ids", [])
        waiting_ids.append(token.current_transition.id)
        token.process_context.scope["waiting_ids"] = waiting_ids
    else:
        total = token.process_context.scope.get("total", 0)
        token.process_context.scope["total"] = total + input
        logger.info(
            "Current {current}, Total: {total}".format(
                current=input, total=total + input
            )
        )
        next_(token)


@delegateify
def a3_1(next_, token):
    print("a3_1")
    total = token.process_context.scope.get("total", 0)
    current = token.environ.get("price1", 0)
    token.process_context.scope["total"] = total + current
    next_(token)


@delegateify
def a3_2(next_, token):
    print("a3_2")
    total = token.process_context.scope.get("total", 0)
    current = token.environ.get("price2", 0)
    token.process_context.scope["total"] = total + current
    next_(token)


def prepare_log_feature(writer=None):
    logger = LogFeature()
    if writer is None:
        writer = StreamWriter()
    logger.set_writer(writer)
    logger.set_format("[%(level)s] [%(time)s] - %(message)s")

    return logger


def pause_and_continute(writer=None):
    return (
        ProcessBuilder()
        .add_activity("a1")
        .add_activity("a2")
        .add_execution("a2", a2)
        .add_transition("a1", "a2")
        .add_activity("a3")
        .add_execution("a3", a3_1)
        .add_execution("a3", a3_2)
        .add_transition("a1", "a3")
        .add_activity("a4")
        .add_transition("a2", "a4")
        .add_transition("a3", "a4")
        .set_start("a1")
        .use_feature("logger", prepare_log_feature(writer))
        .build()
    )
