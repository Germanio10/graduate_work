from pydantic import BaseModel


class UserQuestion(BaseModel):
    text: str
