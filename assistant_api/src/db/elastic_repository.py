from functools import lru_cache

from db.abstract_repository import AbstractRepository
from db.elastic import get_elastic
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from models.film import MainFilmInformation


class ElasticRepository(AbstractRepository):
    def __init__(self, elastic: AsyncElasticsearch):
        self._elastic = elastic

    async def search_film(self, title) -> MainFilmInformation | None:
        body = {
            "query": {"multi_match": {"query": title, "fields": ["title"]}},
            "size": 1,
        }
        try:
            doc = await self._elastic.search(index='movies', body=body)
            answer = MainFilmInformation(**doc['hits']['hits'][0]['_source'])
            return answer
        except (NotFoundError, IndexError):
            return None

    async def films_by_actor(self, actor_name) -> list[str] | None:
        body = {
            "query": {"multi_match": {"query": actor_name, "fields": ["actors_names"]}},
            "size": 1000,
            "_source": ["title"],
        }
        try:
            doc = await self._elastic.search(index='movies', body=body)
            film_titles = [hit['_source']['title'] for hit in doc['hits']['hits']]
            return film_titles
        except NotFoundError:
            return None

    async def films_amount(self, director_name) -> tuple[int, list[str]] | None:
        body = {
            "query": {"multi_match": {"query": director_name, "fields": ["directors_names"]}},
            "size": 1000,
            "_source": ["title"],
        }
        try:
            doc = await self._elastic.search(index='movies', body=body)
            film_titles = [hit['_source']['title'] for hit in doc['hits']['hits']]
            count = len(film_titles)
            return count, film_titles
        except NotFoundError:
            return None


@lru_cache()
def get_db_repository(
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> AbstractRepository:
    return ElasticRepository(elastic=elastic)
