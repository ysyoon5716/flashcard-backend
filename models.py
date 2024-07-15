from pydantic import BaseModel

class Deck(BaseModel):
    deck_id: str
    name: str


class Card(BaseModel):
    card_id: str
    deck_id: str
    front: str
    back: str