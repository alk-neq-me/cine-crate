from aioredis import Redis, from_url


async def redis_connect() -> Redis:
    redis = from_url("redis://localhost")
    await redis.set("cinecrate", "hello, world")
    return redis
