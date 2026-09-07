from pydantic import BaseModel


class Lider(BaseModel):
    name: str
    score: int
