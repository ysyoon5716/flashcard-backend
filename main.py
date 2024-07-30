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
    card.id = str(uuid.uuid4())
    cards.insert_one(card.dict())
    return card


@app.get('/card/{id}')
def read_card(id: str) -> Card:
    cards = mongo_client["flashcard"]["cards"]
    card = cards.find_one({"id": id})
    return card


@app.delete('/card/{id}')
def delete_card(id: str):
    cards = mongo_client["flashcard"]["cards"]
    cards.delete_one({"id": id})
    return {"message": "Card deleted"}


@app.put('/card/{id}')
def update_card(id: str, card: Card) -> Card:
    card.id = id
    cards = mongo_client["flashcard"]["cards"]
    cards.update_one({"id": id}, {"$set": card.dict()})
    return card


@app.get('/card/random')
def read_random_card() -> Card:
    cards = mongo_client["flashcard"]["cards"]
    card = cards.aggregate([{"$sample": {"size": 1}}])
    return list(card)[0]