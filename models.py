from pydantic import BaseModel

class Card(BaseModel):
    id: str | None = None
    front: str
    back: str