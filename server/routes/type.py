from typing import Union
from pydantic import BaseModel, Field


class Movie(BaseModel):
    id: Union[str, int]
    title: str = Field(max_length=64)
    overview: str = Field(max_length=1000)
    link: Union[str, None] = Field(max_length=127, default=None)
    poster: str = Field(max_length=127)
