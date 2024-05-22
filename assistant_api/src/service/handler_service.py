from functools import lru_cache

from db.abstract_cache_repository import AbstractCacheRepository
from db.abstract_repository import AbstractRepository
from db.redis_cache import get_cache_repository
from db.remote_repository import get_remote_repository
from fastapi import Depends
from models.film import MainFilmInformation
from models.user_question import UserQuestion


class HandlerService:
    def __init__(self, db: AbstractRepository, cache: AbstractCacheRepository) -> None:
        self._db = db
        self._cache = cache

    async def execute(self, question: UserQuestion) -> str:
        await self._cache.set('dfdf', 'dsdsds')
        if 'movie' in question.text:
            title = question.text.split()[-1]
            film: MainFilmInformation = await self._db.search_film(title=title)
            if 'rating' in question.text:
                raiting = film.imdb_rating
                return f'Рейтинг фильма {title} {raiting}'
            if 'genre' in question.text:
                genre_names = ''.join([genre.name for genre in film.genre])
                return f'Жанры фильма {title} {genre_names}'
        else:
            return 'Ничего не найдено'


@lru_cache
def get_handler_service(
    db: AbstractRepository = Depends(get_remote_repository),
    cache: AbstractCacheRepository = Depends(get_cache_repository),
) -> HandlerService:
    return HandlerService(db=db, cache=cache)
