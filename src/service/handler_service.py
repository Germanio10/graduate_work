from functools import lru_cache

from db.abstract_repository import AbstractRepository, get_db
from fastapi import Depends
from models.film import MainFilmInformation
from models.user_question import UserQuestion


class HandlerService:
    def __init__(self, db: AbstractRepository) -> None:
        self.db = db

    async def execute(self, question: UserQuestion) -> str:
        if 'movie' in question.text:
            title = question.text.split()[-1]
            film: MainFilmInformation = await self.db.search_film(title=title)
            print(film)
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
    db: AbstractRepository = Depends(get_db),
) -> HandlerService:
    return HandlerService(db=db)
