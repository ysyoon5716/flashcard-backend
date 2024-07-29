import os
import uuid
import pymongo
from typing import List
from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models import *

load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

mongo_client = pymongo.MongoClient(
    os.getenv("MONGO_URL"), 
    username=os.getenv("MONGO_USERNAME"),
    password=os.getenv("MONGO_PASSWORD"),
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/decks")
def read_decks() -> List[Deck]:
    decks = mongo_client["flashcard"]["decks"]
    decks = [Deck(**deck) for deck in decks.find()]
    return decks


@app.post('/decks/create')
def create_deck(deck: Deck):
    deck.deck_id = str(uuid.uuid4())
    decks = mongo_client["flashcard"]["decks"]
    decks.insert_one(deck.dict())
    return {"status": "ok"}


@app.post('/decks/delete')
def delete_deck(deck: Deck):
    decks = mongo_client["flashcard"]["decks"]
    decks.delete_one({"deck_id": deck.deck_id})

    cards = mongo_client["flashcard"]["cards"]
    cards.delete_many({"deck_id": deck.deck_id})
    return {"status": "ok"}


@app.post('/decks/update')
def update_deck(deck: Deck):
    decks = mongo_client["flashcard"]["decks"]
    decks.update_one({"deck_id": deck.deck_id}, {"$set": {"name": deck.name}})
    return {"status": "ok"}


@app.get('/decks/{deck_id}')
def read_deck(deck_id: str) -> List[Card]:
    cards = mongo_client["flashcard"]["cards"]
    cards = [Card(**card) for card in cards.find({"deck_id": deck_id})]
    return cards


@app.post('/cards/create')
def create_card(card: Card):
    cards = mongo_client["flashcard"]["cards"]
    card.card_id = str(uuid.uuid4())
    cards.insert_one(card.dict())
    return {"status": "ok"}


@app.get('/cards/delete')
def delete_card(card_id: str):
    cards = mongo_client["flashcard"]["cards"]
    cards.delete_one({"card_id": card_id})
    return {"status": "ok"}


@app.post('/cards/update')
def update_card(card: Card):
    cards = mongo_client["flashcard"]["cards"]
    cards.update_one({"card_id": card.card_id}, {"$set": {"front": card.front, "back": card.back}})
    return {"status": "ok"}