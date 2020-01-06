import os
import pytest

from pvm import ProcessBuilder, delegateify
from pvm.features.logging import LogFeature, StreamWriter


@delegateify
def a1(next_, token):
    total = token.process_context.scope.get("total", 0)
    token.process_context.logger.info("Current: %d", total)
    token.process_context.scope["total"] = total + 1
    next_(token)


@delegateify
def a2(next_, token):
    total = token.process_context.scope.get("total", 0)
    token.process_context.logger.info("Total: %d", total)
    next_(token)


def set_predicate(cycle):
    cycle.set_predicate(lambda t: t.process_context.scope.get("total", 0) < 3)


def prepare_log_feature(writer=None):
    logger = LogFeature()
    if writer is None:
        writer = StreamWriter()
    logger.set_writer(writer)
    logger.set_format("[%(level)s] [%(time)s] - %(message)s")

    return logger


def test_cycle(capsys):
    process = (
        ProcessBuilder()
        .add_activity("a1", set_predicate, "Cycle")
        .add_execution("a1", a1)
        .add_activity("a2")
        .add_execution("a2", a2)
        .add_transition("a1", "a2")
        .set_start("a1")
        .use_feature("logger", prepare_log_feature())
        .build()
    )

    process.start({})

    expected = [
        "occurs.",
        "is ready to execute.",
        "Current: 0",
        "finished ths executions.",
        "passed.",
        "is ready to execute.",
        "Current: 1",
        "finished ths executions.",
        "passed.",
        "is ready to execute.",
        "Current: 2",
        "finished ths executions.",
        "passed.",
        "is ready to execute.",
        "Total: 3",
    ]

    out, err = capsys.readouterr()
    lines = err.split(os.linesep)

    for i, e in enumerate(expected):
        assert lines[i].split("-")[-1].strip().endswith(e)
