from core import log


def test_log_info():
    log.info("string info")


def test_log_err():
    log.err("string err")


def test_log_warn():
    log.warn("string warn")
