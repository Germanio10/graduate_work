from abc import ABC, abstractmethod

from models.film import MainFilmInformation


class AbstractRepository(ABC):

    @abstractmethod
    def search_film(self, title) -> MainFilmInformation:
        pass
