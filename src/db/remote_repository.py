from db.abstract_repository import AbstractRepository
from db.api_client import ApiClient
from fastapi import Depends
from models.film import MainFilmInformation
from models.ganre import Genre


class RemoteRepository(AbstractRepository):
    def __init__(self, api_client: ApiClient) -> None:
        self.api_client = api_client

    async def search_film(self, title, **kwargs) -> MainFilmInformation:
        response = await self.api_client.get(path='films/search', search=title)
        film = response['results'][0]
        print(film)

        # main_film = MainFilmInformation(
        #     id=film['id'],
        #     title=film['title'],
        #     imdb_rating=film['imdb_rating'],
        #     genres_list=[Genre(**genre) for genre in film['genres_list']],
        # )

        return MainFilmInformation(**film)
