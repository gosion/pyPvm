import pytest

from tests.processes import pause_and_continute


def test_builder():
    process = pause_and_continute()

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
