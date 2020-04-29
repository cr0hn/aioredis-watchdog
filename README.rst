Redis Watchdog for Python
=========================

This project allow to monitor Redis keys for changes and launch callbacks.

Install
=======

.. code-block:: console

    $ pip install aioredis-watchdog


Concepts
========

Redis pattern
-------------

You can configure which Redis keys you wish to watch by using a *redis pattern*.

Callbacks
---------

Each time a key was changed in Redis, `aioredis-watchdog` will call the list of callbacks.

Using as library
================

For monitoring all Redis keys that starts by *user-*:

.. code-block:: python

    import asyncio

    from aioredis_watchdog import watchdog

    async def callback1(key: str, data: bytes):
        print("Key callback 1: ", key, "#", data)

    async def callback2(key: str, data: bytes):
        print("Key callback 2: ", key, "#", data)

    async def monitoring(connection_string: str):
        redis = await aioredis.create_redis_pool(connection_string)

        callbacks = [callback1, callback2]

        await watchdog("user-*", callbacks, redis)

    asyncio.run(monitoring("redis://localhost"))

Callbacks must have this signature:

.. code-block:: python

    async def FUNCTION_NAME(KEY: str, VALUE: bytes):
        ...

Where:

- Function is a coroutine
- KEY: is the key name in redis and is plain string
- VALUE: is the value for this key in Redis. It's in bytes format.

