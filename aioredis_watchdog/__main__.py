import asyncio
import argparse

import aioredis

from aioredis_watchdog import watchdog


async def callback(key, value):
    print("[*] Modified key: ", key, "#", value)


async def _main(args):
    # Connect with redis
    redis = await aioredis.create_redis_pool(args.connection_string)

    print(f"[*] Starting monitoring '{args.connection_string}'")

    await watchdog("*", [callback], redis)


def main():
    parser = argparse.ArgumentParser(
        description='Redis Watchdog cli'
    )
    parser.add_argument("-s", "--connection-string",
                        default="redis://localhost",
                        help="redis connection string")

    parsed = parser.parse_args()

    asyncio.run(_main(parsed))


if __name__ == '__main__':
    main()
