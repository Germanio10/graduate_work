from functools import lru_cache

from db.abstract_repository import AbstractRepository
from db.api_client import ApiClient, get_api_client
from fastapi import Depends
from models.film import MainFilmInformation


class RemoteRepository(AbstractRepository):
    def __init__(self, api_client: ApiClient) -> None:
        self.api_client = api_client

    async def search_film(self, title, **kwargs) -> MainFilmInformation | None:
        response = await self.api_client.get(path='films/search', search=title)
        if not film:
            return None
        film = response['results'][0]

        return MainFilmInformation(**film)


@lru_cache()
def get_remote_repository(
    api_client: ApiClient = Depends(get_api_client),
) -> AbstractRepository:
    return RemoteRepository(api_client=api_client)
