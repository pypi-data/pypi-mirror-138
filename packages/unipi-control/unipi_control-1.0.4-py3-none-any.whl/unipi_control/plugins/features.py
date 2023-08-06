import asyncio
from asyncio import Task
from contextlib import AsyncExitStack
from typing import Any
from typing import AsyncIterable
from typing import Set

from config import LOG_MQTT_PUBLISH
from config import LOG_MQTT_SUBSCRIBE
from config import LOG_MQTT_SUBSCRIBE_TOPIC
from config import logger


class FeaturesMqttPlugin:
    """Provide features control as MQTT commands."""

    def __init__(self, uc, mqtt_client):
        self._uc = uc
        self._mqtt_client = mqtt_client

    async def init_tasks(self, stack: AsyncExitStack) -> Set[Task]:
        tasks: Set[Task] = set()

        for feature in self._uc.neuron.features.by_feature_type(["DO", "RO"]):
            topic: str = f"{feature.topic}/set"

            manager = self._mqtt_client.filtered_messages(topic)
            messages = await stack.enter_async_context(manager)

            subscribe_task: Task[Any] = asyncio.create_task(self._subscribe(feature, topic, messages))
            tasks.add(subscribe_task)

            await self._mqtt_client.subscribe(topic)
            logger.debug(LOG_MQTT_SUBSCRIBE_TOPIC, topic, extra={"markup": True})

        for feature in self._uc.neuron.features.by_feature_type(["AO", "DI", "DO", "RO"]):
            publish_task: Task[Any] = asyncio.create_task(self._publish(feature))
            tasks.add(publish_task)

        return tasks

    @staticmethod
    async def _subscribe(feature, topic: str, messages: AsyncIterable):
        async for message in messages:
            value: str = message.payload.decode()

            if value == "ON":
                await feature.set_state(1)
            elif value == "OFF":
                await feature.set_state(0)

            logger.info(LOG_MQTT_SUBSCRIBE, topic, value, extra={"markup": True})

    async def _publish(self, feature):
        while True:
            if await feature.changed:
                topic: str = f"{feature.topic}/get"
                state: str = await feature.state
                await self._mqtt_client.publish(topic, state, qos=1, retain=True)
                logger.info(LOG_MQTT_PUBLISH, topic, state, extra={"markup": True})

            await asyncio.sleep(25e-3)
