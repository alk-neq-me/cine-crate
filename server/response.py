from typing import Generic, List, TypeVar
from pydantic import BaseModel

from routes.type import Movie


class HttpResponse(BaseModel):
    status: int
    message: str


T = TypeVar("T")

class HttpResponseMovies(BaseModel, Generic[T]):
    status: int
    data: List[T]
    count: int
