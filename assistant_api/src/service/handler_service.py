from functools import lru_cache

import spacy
from db.abstract_cache_repository import AbstractCacheRepository
from db.abstract_repository import AbstractRepository
from db.elastic_repository import get_db_repository
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
                    genre_names = ' '.join(film.genre)
                    return f'жанры фильма {search_param} {genre_names}'
                case 'director':
                    director_names = ' '.join(film.directors_names)
                    return f'режиссер фильма {search_param} {director_names}'
                case _:
                    actor_films = await self._db.films_by_actor(actor_name=search_param)
                    return f'{search_param} снимался в фильмах: {actor_films}'
                
        elif type_ == '':
                match 'tag':
                    case 'actor':
                        actor_films = await self._db.films_by_actor(actor_name=search_param)
                        return f'Актер {search_param} снимался в фильмах: {", ".join(actor_films)}'
        elif type_ == '':
                match 'tag':
                    case 'director':
                        count, films = await self._db.films_amount(director_name=search_param)
                        count_text = self.get_film_count_text(count)
                        return f'{search_param} снял {count_text}: {", ".join(films)}'
        return 'Ничего не найдено'
    
    @staticmethod
    def get_film_count_text(count: int) -> str:
        if count % 10 == 1 and count % 100 != 11:
            return f"{count} фильм"
        elif 2 <= count % 10 <= 4 and (count % 100 < 10 or count % 100 >= 20):
            return f"{count} фильма"
        else:
            return f"{count} фильмов"

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
    db: AbstractRepository = Depends(get_db_repository),
    cache: AbstractCacheRepository = Depends(get_cache_repository),
) -> HandlerService:
    return HandlerService(db=db, cache=cache)
