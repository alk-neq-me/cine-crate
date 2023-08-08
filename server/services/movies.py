from typing import List, Optional, Union
from aiohttp import ClientSession

from routes.type import Movie
from settings import settings
from utils import SortByEnum


headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {settings.TMDB_AUTH_TOKEN}"
}

async def fetch_now_playing_movies(
    page: int = 1,
    region: Optional[str] = None,
    ) -> List[Movie]:
    async with ClientSession(headers=headers) as session:
        async with session.get(f"https://api.themoviedb.org/3/movie/now_playing?language=en-US&page={page}{f'&region={region}' if region else ''}") as response:
            movies = await response.json()
            return [Movie(id=movie["id"], title=movie["title"], overview=movie["overview"], poster=f"https://image.tmdb.org/t/p/w500/{movie['poster_path']}") for movie in movies["results"]]


async def fetch_popular_movies(
    page: int = 1,
    region: Optional[str] = None,
    ) -> List[Movie]:
    async with ClientSession(headers=headers) as session:
        async with session.get(f"https://api.themoviedb.org/3/movie/popular?language=en-US&page={page}{f'&region={region}' if region else ''}") as response:
            movies = await response.json()
            return [Movie(id=movie["id"], title=movie["title"], overview=movie["overview"], poster=f"https://image.tmdb.org/t/p/w500/{movie['poster_path']}") for movie in movies["results"]]


async def fetch_top_rated_movies(
    page: int = 1,
    region: Optional[str] = None,
    ) -> List[Movie]:
    async with ClientSession(headers=headers) as session:
        async with session.get(f"https://api.themoviedb.org/3/movie/top_rated?language=en-US&page={page}{f'&region={region}' if region else ''}") as response:
            movies = await response.json()
            return [Movie(id=movie["id"], title=movie["title"], overview=movie["overview"], poster=f"https://image.tmdb.org/t/p/w500/{movie['poster_path']}") for movie in movies["results"]]


async def fetch_upcoming_movies(
    page: int = 1,
    region: Optional[str] = None,
    ) -> List[Movie]:
    async with ClientSession(headers=headers) as session:
        async with session.get(f"https://api.themoviedb.org/3/movie/upcoming?language=en-US&page={page}{f'&region={region}' if region else ''}") as response:
            movies = await response.json()
            return [Movie(id=movie["id"], title=movie["title"], overview=movie["overview"], poster=f"https://image.tmdb.org/t/p/w500/{movie['poster_path']}") for movie in movies["results"]]


async def fetch_movie_by_id(id: Union[str, int]) -> Movie:
    async with ClientSession(headers=headers) as session:
        async with session.get(f"https://api.themoviedb.org/3/movie/{id}?language=en-US") as response:
            movie = await response.json()
            return Movie(id=movie["id"], title=movie["title"], overview=movie["overview"], poster=f"https://image.tmdb.org/t/p/w500/{movie['poster_path']}")


async def fetch_movies_by_genres(
    include_adult: bool = False,
    page: int = 1,
    region: Optional[str] = "",
    year: Optional[str] = None,
    genres: str = "",
    sort_by: SortByEnum = SortByEnum.POPULARITY_ASC
    ) -> Movie:
    async with ClientSession(headers=headers) as session:
        async with session.get(f"https://api.themoviedb.org/3/discover/movie?include_adult={include_adult}&region={region}&include_video=false&language=en-US&page={page}&year={year}&sort_by={sort_by}&with_genres={genres}") as response:
            movies = await response.json()
            return [Movie(id=movie["id"], title=movie["title"], overview=movie["overview"], poster=f"https://image.tmdb.org/t/p/w500/{movie['poster_path']}") for movie in movies["results"]]


async def fetch_search_movie(
    query: str,
    include_adult: bool = False,
    page: int = 1,
    region: Optional[str] = None,
    year: Optional[str] = None,
    primary_release_year: Optional[str] = None,
) -> List[Movie]:
    async with ClientSession(headers=headers) as session:
        async with session.get(f"https://api.themoviedb.org/3/search/movie?query={query}&include_adult={include_adult}&language=en-US&primary_release_year={primary_release_year}&page={page}&region={region}&year={year}") as response:
            movies = await response.json()
            return [Movie(id=movie["id"], title=movie["title"], overview=movie["overview"], poster=f"https://image.tmdb.org/t/p/w500/{movie['poster_path']}") for movie in movies["results"]]
