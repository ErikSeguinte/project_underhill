from enum import Enum
from pydantic import BaseModel


class CardType(str, Enum):
    relationship = "relationship"
    possession = "possession"
    action = "action"
    feeling = "feeling"


class UserBase(BaseModel):
    email: str
    secret_question: str

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str
    secret_answer: str


class UserVerify(UserCreate):
    id: str
    pass


class User(UserBase):
    id: str


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

    class Config:
        orm_mode = True


class CardCreate(CardBase):
    pass


class Card(CardBase):
    pass


class PlayerState(int, Enum):
    not_ready = 0
    ready = 1
    waiting = 2
    complete = 3


class PlayerType(str, Enum):
    child = "child"
    changeling = "changeling"
