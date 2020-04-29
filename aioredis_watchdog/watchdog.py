import asyncio

from typing import List, Callable

import aioredis


async def watchdog(redis_pattern: str,
                   callbacks: List[Callable],
                   redis_connection: aioredis.commands.Redis):
    """
    Usage:

    >>> async def print_modified(key: str, value: bytes):
            print("Key: ", key, "- Value", value)
    >>> await watchdog("*", print_modified, redis)
    """
    # Config redis for callbacks
    await redis_connection.config_set("notify-keyspace-events", "KEA")

    mpsc = aioredis.pubsub.Receiver()
    await redis_connection.psubscribe(mpsc.pattern(redis_pattern))

    async for channel, msg in mpsc.iter():
        value, operation = msg

        if operation == b"set":
            _value = value.decode("UTF-8")
            modified_key = _value[_value.rfind(":") + 1:]
            modified_value = await redis_connection.get(modified_key)

            for cb in callbacks:
                asyncio.create_task(cb(modified_key, modified_value))


__all__ = ("watchdog",)
