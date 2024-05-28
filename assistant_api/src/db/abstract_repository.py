from abc import ABC, abstractmethod

from models.film import MainFilmInformation


class AbstractRepository(ABC):

    @abstractmethod
    def search_film(self, title) -> MainFilmInformation:
        pass

    @abstractmethod
    def films_by_actor(self, title) -> list[str]:
        pass
    
    @abstractmethod
    def films_amount(self, title) -> list[str]:
        pass
    