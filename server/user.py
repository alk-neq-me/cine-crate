from typing import Optional
from uuid import uuid4
from pydantic import UUID4, BaseModel, Field, SecretStr
from settings import settings
from aioredis import Redis
from base64 import b64decode, b64encode
import bcrypt
import secrets


class UserInput(BaseModel):
    email: str = Field(max_length=128)
    password: str = Field(min_length=4, max_length=16)


class UserScheme(BaseModel):
    id: UUID4 = Field(default_factory=uuid4)
    username: str = Field(max_length=64)
    password: SecretStr
    email: str = Field(max_length=128)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.password = self._hash_password(self.password.get_secret_value())

    @classmethod
    def _hash_password(cls, password: str) -> SecretStr:
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return SecretStr(hashed_password.decode('utf-8'))

    def verify_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), self.password.get_secret_value().encode('utf-8'))


async def encode_user(redis: Redis, user: UserScheme) -> str:
    encoded = b64encode(user.model_dump_json().encode("utf-8"))
    token = secrets.token_hex() 
    await redis.set(token, encoded, ex=settings.REDIS_EXPIRY)
    return token


# from database, hashed
async def create_guest_user(redis: Redis) -> UserScheme:
    """GUEST is session user"""
    user = UserScheme(username=secrets.token_hex(), password=secrets.token_hex()[16], email=f"guest-{secrets.token_hex()}@cine-crate.com")
    await redis.set(f"guest:{user.email}", user.model_dump_json(), ex=settings.REDIS_EXPIRY)

    return user


async def get_guest_user(redis: Redis, email: str) -> Optional[UserScheme]:
    user = await redis.get(f"guest:{email}")
    if not user:
        return None
    user = UserScheme.model_validate_json(user)

    return user


async def get_current_guest_user(redis: Redis, token: str) -> Optional[UserScheme]:
    raw = await redis.get(token)
    if not raw:
        return None
    decoded = b64decode(raw)

    user = UserScheme.model_validate_json(decoded)
    return user



if __name__ == "__main__":
    import asyncio
    from aioredis import Redis, from_url
    async def main():
        redis = from_url("redis://localhost")
        id = "fc5f6b3d-3513-11ee-aa2d-c9b836c6754a"
        print(await get_guest_user(redis, id))

    asyncio.run(main())
