from typing import Optional
from fastapi import HTTPException, Request
from pydantic import BaseModel, Field

from user import UserScheme, get_current_guest_user, get_guest_user, settings
from utils import SortByEnum


class CommonQuery(BaseModel):
    page: int = Field(default=1)
    region: Optional[str] = None


class CategoryMovieQuery(BaseModel):
    include_adult: bool = Field(default=False)
    page: int = Field(default=1)
    region: str = ""
    year: Optional[str] = None
    genres: str = ""
    sort_by: SortByEnum = SortByEnum.POPULARITY_ASC


class SearchMovieQuery(BaseModel):
    query: str = Field(max_length=64)
    include_adult: bool = Field(default=False)
    primary_release_year: Optional[str] = None
    page: int = Field(default=1)
    region: Optional[str] = None
    year: Optional[str] = None


async def guest_user_security_deps(request: Request) -> UserScheme:
    redis = request.app.state.redis_pool
    token = request.cookies.get("token")
    if not token:
        raise HTTPException(status_code=403, detail="Invalid token")

    input_user = await get_current_guest_user(redis, token)
    if not input_user:
        raise HTTPException(status_code=403, detail="Invalid user")

    # check still valid in session
    session_user = await get_guest_user(redis, input_user.email)
    if not session_user:
        raise HTTPException(status_code=403, detail="User not found")

    if input_user.username == session_user.username and input_user.email == session_user.email:
        return input_user

    raise HTTPException(403)


async def active_user(request: Request):
    from aioredis import Redis
    redis: Redis = request.app.state.redis_pool
    token = request.cookies.get("token")
    if not token:
        raise HTTPException(status_code=403, detail="Invalid token")
    input_user = await get_current_guest_user(redis, token)
    if not input_user:
        raise HTTPException(status_code=403, detail="Invalid user")

    await redis.expire(f"guest:{input_user.email}", settings.REDIS_EXPIRY)
