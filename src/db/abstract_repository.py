from abc import ABC, abstractmethod

from models.film import MainFilmInformation


class AbstractRepository(ABC):

    @abstractmethod
    def search_film(self, title) -> MainFilmInformation:
        pass


db: AbstractRepository | None = None


def get_db() -> AbstractRepository | None:
    return db
