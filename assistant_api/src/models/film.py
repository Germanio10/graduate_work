from models.ganre import Genre
from pydantic import BaseModel


class MainFilmInformation(BaseModel):
    id: str
    title: str
    imdb_rating: float | None
    genre: list[str] | None
