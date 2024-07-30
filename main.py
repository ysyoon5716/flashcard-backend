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



@app.get('/cards')
def read_cards() -> List[Card]:
    cards = mongo_client["flashcard"]["cards"]
    cards = list(cards.find())
    return cards


@app.post('/card')
def create_card(card: Card) -> Card:
    cards = mongo_client["flashcard"]["cards"]
    card.card_id = str(uuid.uuid4())
    cards.insert_one(card.dict())
    return card


@app.get('/card/{card_id}')
def read_card(card_id: str) -> Card:
    cards = mongo_client["flashcard"]["cards"]
    card = cards.find_one({"card_id": card_id})
    return card


@app.delete('/card/{card_id}')
def delete_card(card_id: str):
    cards = mongo_client["flashcard"]["cards"]
    cards.delete_one({"card_id": card_id})
    return {"message": "Card deleted"}


@app.put('/card/{card_id}')
def update_card(card_id: str, card: Card) -> Card:
    cards = mongo_client["flashcard"]["cards"]
    cards.update_one({"card_id": card_id}, {"$set": card.dict()})
    return card