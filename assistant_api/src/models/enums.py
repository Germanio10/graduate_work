from enum import Enum


class ConextTypeEnum(str, Enum):
    movie = 'MOVIE'
    actor = 'ACTOR'
    director = 'DIRECTOR'


class TagEnum(str, Enum):
    rating = 'rating'
    genres = 'genres'
    director = 'director'
