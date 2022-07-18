from asyncio_mqtt import Client


class Mqtt:
    """Class for modules IPC with mqtt message broker"""

    _DEFAULT_HOSTNAME = "localhost"
    _DEFAULT_PORT = 1883

    def __init__(
        self,
        hostname=_DEFAULT_HOSTNAME,
        port=_DEFAULT_PORT,
        username=None,
        password=None,
    ):

        self._hostname = hostname
        self._port = port
        self._username = username
        self._password = password

        self._client = Client(hostname, port, username=username, password=password)

    async def __aenter__(self):
        self._client = await self._client.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self._client.__aexit__(exc_type, exc, tb)

    def _get_client(self):
        return self._client

    async def publish(self, topic, message):
        return await self._client.publish(topic, payload=message.encode())

    async def subscribe(self, topic):
        await self._client.subscribe(f"{topic}/#")
        return self._client.filtered_messages(f"{topic}/+")
