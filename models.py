from pydantic import BaseModel

class Card(BaseModel):
    card_id: str | None = None
    front: str
    back: str