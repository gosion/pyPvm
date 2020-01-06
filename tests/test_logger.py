import os
import pytest
import sys
import time

from pvm.features.logging import LogFeature, StreamWriter, FileWriter

from tests.processes import pause_and_continute


@pytest.fixture
def init():
    file_name = (
        "abc." + time.strftime("%Y%m%d", time.localtime(time.time())) + ".log"
    )

    if os.path.exists(file_name):
        os.remove(file_name)

    yield file_name


def test_log_to_console(capsys):
    process = pause_and_continute(StreamWriter())
    prices = [26, 32, 15]
    initData1 = {
        "price1": prices[0],
        "price2": prices[1],
    }
    process.start(initData1)
    waiting_ids = process.process_context.scope.get("waiting_ids", [])

    assert waiting_ids is not None
    assert len(waiting_ids) == 1
    assert process.process_context.scope.get("total") == (
        prices[0] + prices[1]
    )

    initData2 = {"user_input": 0}
    process.proceed(waiting_ids[0], initData2)

    assert process.process_context.scope.get("total", prices[0] + prices[1])

    initData2["user_input"] = prices[2]
    process.proceed(waiting_ids[0], initData2)

    assert process.process_context.scope.get("total") == (
        prices[0] + prices[1] + prices[2]
    )

    expected = [
        "occurs.",
        "is ready to execute.",
        "inished ths executions.",
        "passed.",
        "is ready to execute.",
        "I am waiting.",
    ]

    out, err = capsys.readouterr()
    lines = err.split(os.linesep)

    for i, e in enumerate(expected):
        assert lines[i].split("-")[-1].strip().endswith(e)


def test_log_to_file(init):
    process = pause_and_continute(FileWriter("abc.log"))

    prices = [26, 32, 15]
    initData1 = {
        "price1": prices[0],
        "price2": prices[1],
    }
    process.start(initData1)
    waiting_ids = process.process_context.scope.get("waiting_ids", [])

    assert waiting_ids is not None
    assert len(waiting_ids) == 1
    assert process.process_context.scope.get("total") == (
        prices[0] + prices[1]
    )

    file_name = init

    initData2 = {"user_input": 0}
    process.proceed(waiting_ids[0], initData2)

    assert process.process_context.scope.get("total", prices[0] + prices[1])

    initData2["user_input"] = prices[2]
    process.proceed(waiting_ids[0], initData2)

    assert process.process_context.scope.get("total") == (
        prices[0] + prices[1] + prices[2]
    )

    expected = [
        "occurs.",
        "is ready to execute.",
        "inished ths executions.",
        "passed.",
        "is ready to execute.",
        "I am waiting.",
    ]

    with open(file_name, mode="r") as f:
        lines = f.readlines()

    for i, e in enumerate(expected):
        assert lines[i].split("-")[-1].strip().endswith(e)
