import re

# todo add other imports
from .alert import AlertPriority
from .weatherData import WeatherData

with open('pyproject.toml', 'r') as f:
    __version__ = re.search(r'^version\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

__all__ = [
    'alert',
    'AlertPriority'
    'bikeData',
    'common_settings',
    'message',
    'mqtt',
    'sensor',
    'weatherData',
    'WeatherData'
]
