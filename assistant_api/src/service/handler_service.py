from functools import lru_cache

import spacy
from core.config import (
    CLASSIFICATOR_MODEL_PATH,
    INTENTS_PATH,
    NER_MODEL_PATH,
    NO_CONTENT,
    NO_FILM_IN_BASE,
    NO_INFO_FILM,
    NO_INTENTS,
    NOT_FOUND,
)
from core.logger import logger
from db.abstract_cache_repository import AbstractCacheRepository
from db.abstract_repository import AbstractRepository
from db.elastic_repository import get_db_repository
from db.redis_cache import get_cache_repository
from fastapi import Depends
from models.enums import ConextTypeEnum, TagEnum
from models.film import MainFilmInformation
from models.user_question import UserQuestion
from service.classificator.nlp_model import AbstractNLP
from service.classificator.question_classificator import get_question_classificator


class HandlerService:
    def __init__(
        self, db: AbstractRepository, cache: AbstractCacheRepository, nlp: AbstractNLP
    ) -> None:
        self._db = db
        self._cache = cache
        self._nlp = nlp

    async def execute(self, question: UserQuestion, user_id: str) -> str:
        context = await self._get_context(question.text, user_id)
        logger.debug('Context %s', context)
        if not context:
            logger.info('No content. question: %s', question.text)
            return NO_CONTENT
        result = self._nlp.classify_question(question.text)
        if not result:
            logger.info('Nо intents. question: %s', question.text)
            return NO_INTENTS

        tag, answer = result
        logger.debug('Tag %s', tag)

        type_, search_param = context
        try:
            if type_ == ConextTypeEnum.movie:
                film: MainFilmInformation = await self._db.search_film(title=search_param)

                if not film:
                    return NO_FILM_IN_BASE
                match tag:
                    case TagEnum.rating:
                        raiting = film.imdb_rating
                        return answer.format(
                            search_param=search_param,
                            raiting=raiting,
                        )
                    case TagEnum.genres:
                        genre_names = ' '.join(film.genre)
                        return answer.format(
                            search_param=search_param,
                            genre_names=genre_names,
                        )
                    case TagEnum.director:
                        director_names = ' '.join(film.directors_names)
                        return answer.format(
                            search_param=search_param,
                            director_names=director_names,
                        )
                    case _:
                        logger.info('Nо film. question: %s', question.text)
                        return NO_INFO_FILM

            elif type_ == ConextTypeEnum.actor:
                actor_films = await self._db.films_by_actor(actor_name=search_param)
                actor_films = ', '.join(actor_films)
                return answer.format(
                    search_param=search_param,
                    actor_films=actor_films,
                )

            elif type_ == ConextTypeEnum.director:
                count, films = await self._db.films_amount(director_name=search_param)
                count_text = self.get_film_count_text(count)
                films = ', '.join(films)
                return answer.format(
                    search_param=search_param,
                    count_text=count_text,
                    films=films,
                )
            logger.info('Nо found. question: %s', question.text)
            return NOT_FOUND
        except KeyError:
            logger.info('Nо found. question: %s', question.text)
            return NOT_FOUND

    @staticmethod
    def get_film_count_text(count: int) -> str:
        if count % 10 == 1 and count % 100 != 11:
            return f"{count} фильм"
        elif 2 <= count % 10 <= 4 and (count % 100 < 10 or count % 100 >= 20):
            return f"{count} фильма"
        else:
            return f"{count} фильмов"

    async def _get_context(self, text: str, user_id: str) -> tuple[str, str] | None:
        result = self._nlp.get_entities(text)
        if not result:
            result: str = await self._cache.get(user_id)
            if not result:
                return None
            label, text = result.split(':')
        else:
            label, text = result[0], result[1]

        await self._cache.set(
            user_id,
            f'{label}:{text}',
        )

        return label, text


@lru_cache
def get_handler_service(
    db: AbstractRepository = Depends(get_db_repository),
    cache: AbstractCacheRepository = Depends(get_cache_repository),
) -> HandlerService:
    return HandlerService(db=db, cache=cache)
