from core import WeatherData

FAKE_WEATHER = {
    "stationId": 10,
    "timestamp": "10:10",
    "windSpeed": 10.10,
    "temperature": 10.10,
    "humidity": 10.10,
    "pressure": 10.10,
    "windDirection": 10.10,
    "latitude": 10.10,
    "longitude": 10.10,
}


class TestWeatherData:
    def test_property(self):
        wd = WeatherData(FAKE_WEATHER)

        assert wd.station_id == 10
