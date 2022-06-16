import time as pytime

from datetime import datetime as dt
from datetime import timezone as tz


class time:
    @classmethod
    def _unix_time(cls):
        return pytime.time()

    @classmethod
    def _human_time(cls, curr=None):
        if curr:
            return dt.fromtimestamp(curr, tz.utc).time()
        else:
            return dt.utcnow().time()

    @classmethod
    def timestamp(cls, curr=None):
        now = curr if curr else cls._unix_time()
        sec, mill = str(now).split(".")

        # truncate secs to millis
        mill = mill[:3]

        return f"{sec}.{mill}"

    @classmethod
    def human_timestamp(cls, curr=None):
        now = cls._human_time(curr)
        hh, mm, ss = str(now).split(":")

        # truncate secs to millis
        ss = ss[:6]

        return f"{hh}:{mm}:{ss}"
