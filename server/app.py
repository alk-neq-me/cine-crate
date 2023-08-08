from typing import Final
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from aioredis import Redis
import time

from routes import movies, guest_user
from response import HttpResponse
from redis_connect import redis_connect


app = FastAPI(
    title="Movie List",
    dependencies=[],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://192.168.100.253:39842"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(movies.router)
app.include_router(guest_user.router)

@app.on_event("startup")
async def startup_event():
    app.state.redis_pool = await redis_connect()


@app.on_event("shutdown")
async def shutdown_event():
    await app.state.redis_pool.close()


@app.middleware("http")
async def add_rate_limit_header(request: Request, call_next) -> JSONResponse:
    """It allows 10 requests per 10 seconds"""
    ALLOWED_REQUEST_COUNT: Final[int] = 60
    ALLOWED_EXPIRY_TIME: Final[int] = 60  # 1 minut

    if not request.client:
        raise HTTPException(status_code=500, detail="Could not determine client host.")

    key = request.client.host
    redis: Redis = app.state.redis_pool

    current_timestamp = int(time.time())

    request_count = await redis.get(key) #  redis.incr(key)

    if not request_count:
        await redis.set(key, 1, ex=ALLOWED_EXPIRY_TIME)
        reset_time = current_timestamp + ALLOWED_EXPIRY_TIME
    else:
        request_count = int(request_count)
        if request_count > ALLOWED_REQUEST_COUNT:
            reset_time = int(await redis.ttl(key)) + current_timestamp
            retry_after = reset_time - current_timestamp
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,  # Correct status code for rate limit exceeded
                content="Rate limit exceeded. Try again later.",
                headers={"Retry-After": str(retry_after)},
            )
        else:
            await redis.incr(key)
            reset_time = current_timestamp + ALLOWED_EXPIRY_TIME

    response = await call_next(request)

    response.headers["X-Rate-Limit-Limit"] = str(ALLOWED_REQUEST_COUNT)  # Adjust this value to your desired rate limit
    response.headers["X-Rate-Limit-Remaining"] = str(ALLOWED_REQUEST_COUNT - (request_count or 0))
    response.headers["X-Rate-Limit-Reset"] = str(reset_time)

    return response


@app.get("/", status_code=status.HTTP_200_OK)
async def root() -> HttpResponse:
    return HttpResponse(status=200, message="hello, movies")
