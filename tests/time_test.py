from core.time import time


def test_human_to_unix():
    now = 1655375124.6186554

    assert time.human_timestamp(now) == "10:25:24.618"
    assert isinstance(time.human_timestamp(), str)


def test_truncated_unix():
    now = 1655375124.6186554

    assert time.timestamp(now) == "1655375124.618"

    assert isinstance(time.timestamp(), str)
    assert float(time.timestamp(now)) == 1655375124.618
