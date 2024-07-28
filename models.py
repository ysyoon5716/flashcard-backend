from pydantic import BaseModel

class Deck(BaseModel):
    deck_id: str | None = None
    name: str

class Card(BaseModel):
    card_id: str | None = None
    deck_id: str | None = None
    front: str
    back: str