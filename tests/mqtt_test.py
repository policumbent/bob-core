import asyncio
import os
import pytest

from core import Mqtt
from core.mqtt import Message

broker = "localhost"
run_local = not os.getenv("CI")
pytest_plugins = "pytest_asyncio"


@pytest.mark.asyncio
@pytest.mark.skipif(
    run_local, reason="This test can be run only with an active mqtt broker"
)
async def test_mqtt_publish():
    async with Mqtt("localhost") as client:
        for i in range(4):
            await client.publish(f"test_topic/ciao{i}", f"test{i}")


@pytest.mark.asyncio
@pytest.mark.skipif(
    run_local, reason="This test can be run only with an active mqtt broker"
)
async def test_mqtt_subscribe():
    async def publisher(num_msg):
        await asyncio.sleep(1)

        async with Mqtt("localhost") as client:
            for i in range(num_msg):
                await client.publish("test_topic/test", f"test{i}")

    async def subscriber(num_msg, count=0):
        async with Mqtt("localhost") as client:
            message_loop = await client.subscribe(f"test_topic")
            async with message_loop as messages:
                async for msg in messages:
                    msg = Message(msg)

                    assert msg.value == f"test{count}"
                    count += 1

                    if count >= num_msg:
                        break

    messages = 20
    await asyncio.gather(subscriber(messages), publisher(messages))


@pytest.mark.asyncio
@pytest.mark.skipif(
    run_local, reason="This test can be run only with an active mqtt broker"
)
async def test_mqtt_sensor_publish():
    async with Mqtt("localhost") as client:
        await client.sensor_publish(f"ant", 12)
        await client.sensor_publish(f"ant", 12.3)
        await client.sensor_publish(f"ant", "12.4")


@pytest.mark.asyncio
@pytest.mark.skipif(
    run_local, reason="This test can be run only with an active mqtt broker"
)
async def test_mqtt_sensor_subscribe():
    sensors = ["acc", "ant/hall", "bme", "altro"]

    async def publisher(num_msg):
        await asyncio.sleep(1)

        async with Mqtt("localhost") as client:

            for _ in range(num_msg // 4):
                await client.sensor_publish(sensors[0], 12)
                await client.sensor_publish(sensors[1], 12.11)
                await client.sensor_publish(sensors[2], 13.11)
                await client.sensor_publish(sensors[3], "hola")

    async def subscriber(num_msg, count=0):
        async with Mqtt("localhost") as client:
            message_loop = await client.sensor_subscribe(sensors)
            async with message_loop as messages:
                async for msg in messages:
                    msg = Message(msg)

                    if msg.sensor == sensors[0]:
                        assert msg.value == 12
                        assert msg.module == None

                    elif msg.sensor == sensors[1]:
                        assert msg.value == 12.11
                        assert msg.module == "ant"

                    elif msg.sensor == sensors[2]:
                        assert msg.value == 13.11
                        assert msg.module == None

                    elif msg.sensor == sensors[3]:
                        assert msg.value == "hola"
                        assert msg.module == None

                    else:
                        assert False

                    count += 1
                    if count >= num_msg:
                        break

    messages = 20
    await asyncio.gather(subscriber(messages), publisher(messages))
