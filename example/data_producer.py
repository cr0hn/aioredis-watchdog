import uuid
import asyncio

import aioredis


async def main():
    redis = await aioredis.create_redis_pool('redis://localhost')

    for x in range(10000):
        v = await redis.set(f'x{x}', uuid.uuid4().hex)
        print("writing: ", x)
        await asyncio.sleep(0.05)


if __name__ == '__main__':
    asyncio.run(main())
