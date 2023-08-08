from typing import Annotated
from fastapi import APIRouter, Body, Request, Response, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from user import UserScheme, create_guest_user, encode_user, get_current_guest_user, get_guest_user
from settings import settings


router = APIRouter(
    prefix="/api/v1/guest-auth",
    tags=["auth"],
    dependencies=[],
    responses={ 404: {"message": "Not found"} }
)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def create_user(request: Request) -> UserScheme:
    redis = request.app.state.redis_pool
    new_user = await create_guest_user(redis)
    return new_user


class LoginUser(BaseModel):
    emial: str = Field(max_length=128)

@router.post("/login", status_code=status.HTTP_200_OK)
async def user_login(loginuser: Annotated[LoginUser, Body(...)], request: Request) -> JSONResponse:
    redis = request.app.state.redis_pool
    token = request.cookies.get("token")

    if token:
        return JSONResponse(content={"message": "Current user exists"}, status_code=401, headers={"Location": "/api/v1/guest-auth/logout"})

    user = await get_guest_user(redis, loginuser.emial)
    if not user:
        return JSONResponse(content={"message": "Not found user"}, status_code=404)
    token = await encode_user(redis, user)

    response = JSONResponse(
        content={"token": token},
        status_code=200,
    )
    
    response.set_cookie(key="token", value=token, httponly=True, expires=settings.REDIS_EXPIRY)

    return response


@router.delete("/logout", status_code=status.HTTP_200_OK)
async def user_logout(request: Request) -> JSONResponse:
    redis = request.app.state.redis_pool
    token = request.cookies.get("token")
    if not token:
        return JSONResponse(content={"message": "Not login token invalid"}, status_code=404, headers={"Location": "/api/v1/guest-auth/login"})
    user = await get_current_guest_user(redis, token)
    if not user:
        return JSONResponse(content={"message": "Not login, no user"}, status_code=404, headers={"Location": "/api/v1/guest-auth/login"})

    response = JSONResponse(
        content={"message": "success loggout user"},
        headers={"Location": "/api/v1/guest-auth/login"},
        status_code=200,
    )
    
    response.delete_cookie(key="token")
    await redis.delete(token)
    await redis.delete(f"guest:{user.email}")

    return response


# @router.delete("/clean")
# async def clean(res: Response):
#     res.delete_cookie("token")
#     return "ok"
