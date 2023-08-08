from enum import Enum
from typing import Literal, TypeAlias, Union


def to_int(s: Union[str, int]) -> int:
    print(s)
    try:
        return int(s)
    except:
        if type(s) == int:
            return s
        raise Exception("Something wrong")


class SortByEnum(str, Enum):
    POPULARITY_ASC = "popularity.asc"
    POPULARITY_DESC = "popularity.desc"
    REVENUE_ASC = "revenue.asc"
    REVENUE_DESC = "revenue.desc"
    PRIMARY_RELEASE_DATE_ASC = "primary_release_date.asc"
    PRIMARY_RELEASE_DATE_DESC = "primary_release_date.desc"
    VOTE_AVERAGE_ASC = "vote_average.asc"
    VOTE_AVERAGE_DESC = "vote_average.desc"
    VOTE_COUNT_ASC = "vote_count.asc"
    VOTE_COUNT_DESC = "vote_count.desc"


C: TypeAlias = Literal["action", "adventure", "animation", "comedy","crime","documentary","drama","family""fantasy","history","horror","music","mystery","romance","science_fiction"]
def get_genrre_id(category: C) -> int:
    return {
    'action': 28,
    'adventure': 12,
    'animation': 16,
    'comedy': 35,
    'crime': 80,
    'documentary': 99,
    'drama': 18,
    'family': 10751,
    'fantasy': 14,
    'history': 36,
    'horror': 27,
    'music': 10402,
    'mystery': 9648,
    'romance': 10749,
    'science_fiction': 878
}[category]

