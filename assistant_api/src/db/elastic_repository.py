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
            print(doc['hits']['hits'][0]['_source'])
            answer = MainFilmInformation(**doc['hits']['hits'][0]['_source'])
            return answer
        except NotFoundError:
            return None


@lru_cache()
def get_db_repository(
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> AbstractRepository:
    return ElasticRepository(elastic=elastic)
