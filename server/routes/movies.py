from typing import Annotated, List, Union
from aioredis import Redis
from fastapi import APIRouter, Depends, Query, Request, status

from response import HttpResponseMovies
from dependencies import CommonQuery, SearchMovieQuery, CategoryMovieQuery, guest_user_security_deps, active_user
from services.movies import fetch_now_playing_movies, fetch_popular_movies, fetch_movie_by_id, fetch_search_movie, fetch_top_rated_movies, fetch_movies_by_genres
from routes.type import Movie
from recommendation import recommend_by_id, MovieRecommended
from utils import to_int


router = APIRouter(
    prefix="/api/v1",
    tags=["movies"],
    dependencies=[Depends(guest_user_security_deps), Depends(active_user)],
    responses={ 404: {"message": "Not found"} }
)

@router.get("/movies/new_playing", status_code=status.HTTP_200_OK)
async def get_movies_now_playing(q: Annotated[CommonQuery, Depends(CommonQuery)]) -> HttpResponseMovies:
    movies: List[Movie] = await fetch_now_playing_movies(q.page, q.region)
    return HttpResponseMovies(status=status.HTTP_200_OK, data=movies, count=len(movies))


@router.get("/movies/popular", status_code=status.HTTP_200_OK)
async def get_movies_popular(q: Annotated[CommonQuery, Depends(CommonQuery)]) -> HttpResponseMovies:
    movies: List[Movie] = await fetch_popular_movies(q.page, q.region)
    return HttpResponseMovies(status=status.HTTP_200_OK, data=movies, count=len(movies))


@router.get("/movies/top_rated", status_code=status.HTTP_200_OK)
async def get_top_rated(q: Annotated[CommonQuery, Depends(CommonQuery)]) -> HttpResponseMovies:
    movies: List[Movie] = await fetch_top_rated_movies(q.page, q.region)
    return HttpResponseMovies(status=status.HTTP_200_OK, data=movies, count=len(movies))


@router.get("/movies/upcoming", status_code=status.HTTP_200_OK)
async def get_upcoming(q: Annotated[CommonQuery, Depends(CommonQuery)]) -> HttpResponseMovies:
    movies: List[Movie] = await fetch_popular_movies(q.page, q.region)
    return HttpResponseMovies(status=status.HTTP_200_OK, data=movies, count=len(movies))


@router.get("/movie", status_code=status.HTTP_200_OK)
async def get_movie_by_id(
    id: Annotated[Union[str, int], Query(max_length=15)],
    ) -> Movie:
    movie: Movie = await fetch_movie_by_id(id)
    return movie


@router.get("/movies/recommended", status_code=status.HTTP_200_OK)
async def get_movies_recommendation(
    id: int,
    page: int = 1,
    limit: int = 10
    ) -> HttpResponseMovies:
    movies: List[MovieRecommended] = recommend_by_id(to_int(id), page=page, limit=limit)
    return HttpResponseMovies(status=status.HTTP_200_OK, data=movies, count=len(movies))


# @router.get("/redis")
# async def test_resid(request: Request):
#     redis: Redis = request.app.state.redis_pool
#     return {"data": await redis.get("cinecrate")}


@router.get("/movies/category", status_code=status.HTTP_200_OK)
async def get_movies_by_genres(q: Annotated[CategoryMovieQuery, Depends(CategoryMovieQuery)]) -> HttpResponseMovies:
    movies: List[Movie] = await fetch_movies_by_genres(include_adult=q.include_adult, page=q.page, region=q.region, year=q.year, genres=q.genres, sort_by=q.sort_by)
    return HttpResponseMovies(status=status.HTTP_200_OK, data=movies, count=len(movies))


@router.get("/movies/search", status_code=status.HTTP_200_OK)
async def search_movies(q: Annotated[SearchMovieQuery, Depends(SearchMovieQuery)]) -> HttpResponseMovies:
    movies: List[Movie] = await fetch_search_movie(query=q.query, page=q.page, region=q.region, primary_release_year=q.primary_release_year, year=q.year, include_adult=q.include_adult)
    return HttpResponseMovies(status=status.HTTP_200_OK, data=movies, count=len(movies))
