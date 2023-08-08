from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    TMDB_AUTH_TOKEN: str = ""
    REDIS_EXPIRY: int = 2592000

    class Config:
        env_file = "./.env"


settings = Settings()
