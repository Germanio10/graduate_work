from pydantic import BaseModel


class MainFilmInformation(BaseModel):
    id: str
    title: str
    imdb_rating: float | None
    genre: list[str] | None
    directors_names: list[str] | None
