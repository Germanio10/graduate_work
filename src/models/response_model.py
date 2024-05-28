from pydantic import BaseModel


class ResponseAssitant(BaseModel):
    answer: str
