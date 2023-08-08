from typing import List, Union
from pathlib import Path
import pickle

from pydantic import BaseModel


base_dir = Path().parent.absolute()

dataset = pickle.load(open(base_dir / Path("./models/movies.pkl"), "rb"))
similarity = pickle.load(open(base_dir / Path("./models/similarity.pkl"), "rb"))


class MovieRecommended(BaseModel):
    id: Union[str, int]
    title: str
    poster: str


def recommend_by_id(id: int, page: int = 1, limit: int = 10) -> List[MovieRecommended]:
    """Return recommendded movie ids"""
    movie = dataset[dataset["tmdb_id"] == id]

    if movie.empty:
        return []
    idx = movie.index[0]
    dst = similarity[idx]
    lst = sorted(list(enumerate(dst)), reverse=True, key=lambda x: x[1])

    start_idx = (page - 1) * limit
    end_idx = start_idx + limit

    paginated_lst = lst[start_idx:end_idx]

    offset = lambda i: dataset.iloc[i[0]]
    # offset = lambda i: dataset.drop_duplicates(subset="tmdb_id").iloc[i[0]]
    return [ 
        MovieRecommended(id=offset(i).tmdb_id, poster=offset(i).poster, title=offset(i).title)
        for i in paginated_lst
    ]
