import asyncio
import os
import pytest

from core import Mqtt

broker = "localhost"
run_local = not os.getenv("CI")
pytest_plugins = "pytest_asyncio"


@pytest.mark.asyncio
@pytest.mark.skipif(
    run_local, reason="This test can be run only with an active mqtt broker"
)
async def test_mqtt_publish():
    # publish message on topic

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
                    assert msg.payload.decode() == f"test{count}"
                    count += 1

                    if count >= num_msg:
                        break

    messages = 20
    await asyncio.gather(subscriber(messages), publisher(messages))
