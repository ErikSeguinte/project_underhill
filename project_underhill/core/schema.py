from enum import Enum
from pydantic import BaseModel


class CardType(str, Enum):
    relationship = "relationship"
    possession = "possession"


class UserBase(BaseModel):
    email: str
    secret_question: str
    id: str

class UserCreate(UserBase):
    password: str
    secret_answer: str

class User(UserBase):
    pass

class DeckBase(BaseModel):
    owner_id: str

class DeckCreate(DeckBase):
    pass

class DeckBase(DeckBase):
    id: str


class CardBase(BaseModel):
    deck_id: str
    type: CardType
    text: str
    id: int

class CardCreate(BaseModel):
    pass

class Card(BaseModel):
    pass


