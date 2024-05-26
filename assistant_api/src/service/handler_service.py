from functools import lru_cache

import spacy
from db.abstract_cache_repository import AbstractCacheRepository
from db.abstract_repository import AbstractRepository
from db.redis_cache import get_cache_repository
from db.remote_repository import get_remote_repository
from fastapi import Depends
from models.film import MainFilmInformation
from models.user_question import UserQuestion
from utils.classificator.question_classificator import get_question_classificator


class HandlerService:
    def __init__(self, db: AbstractRepository, cache: AbstractCacheRepository) -> None:
        self._db = db
        self._cache = cache
        self._ner = spacy.load('nlp_models/model-best')
        self._question_classificator = get_question_classificator(
            'nlp_models/classificator.pth',
            'nlp_models/intents.json',
        )

    async def execute(self, question: UserQuestion) -> str:
        context = await self._get_context(question.text)
        print(f'{context=}')
        if not context:
            return 'Извините но не хватает контекста'
        tag = self._question_classificator.classify_question(question.text)
        print(f'{tag=}')
        if not tag:
            return 'Извините но мы можем подскзать только о нашей коллеции фильмов'

        type_, search_param = context

        if type_ == 'MOVIE':
            film: MainFilmInformation = await self._db.search_film(title=search_param)

            if not film:
                return 'Извините но такого фильма у нас нет'

            match tag:
                case 'rating':
                    raiting = film.imdb_rating
                    return f'рейтинг фильма {search_param} {raiting}'
                case 'genres':
                    genre_names = ''.join([genre.name for genre in film.genre])
                    return f'жанры фильма {search_param} {genre_names}'
                case _:
                    return f'рейтинг фильма {search_param} {raiting}'

        return 'Ничего не найдено'

    async def _get_context(self, text: str, user_id: int = '245') -> tuple[str, str] | None:
        doc = self._ner(text)
        if not doc.ents:
            result = await self._cache.get(user_id)
            if not result:
                return None

        label, text = doc.ents[0].label_, doc.ents[0].text

        await self._cache.set(
            user_id,
            f'{label}:{text}',
        )

        return label, text


@lru_cache
def get_handler_service(
    db: AbstractRepository = Depends(get_remote_repository),
    cache: AbstractCacheRepository = Depends(get_cache_repository),
) -> HandlerService:
    return HandlerService(db=db, cache=cache)
