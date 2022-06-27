import re

from .bikeData import BikeData
from .common_settings import CommonSettings
from .message import Message
from .mqtt import Mqtt
from .sensor import Sensor
from .weatherData import WeatherData
from .log import log
from .database import *
from .time import *

from .exceptions import *

__all__ = [
    # module import
    "bikeData",
    "common_settings",
    "message",
    "mqtt",
    "sensor",
    "weatherData",
    "exceptions",
    "database",
    "time"
    # class import
    "BikeData",
    "CommonSettings",
    "Message",
    "Mqtt",
    "Sensor",
    "WeatherData",
    "log",
]


try:
    with open("pyproject.toml", "r") as f:
        __version__ = re.search(
            r'^version\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE
        ).group(1)
except FileNotFoundError:
    __version__ = "0.1.0"
