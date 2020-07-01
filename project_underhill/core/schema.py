from enum import Enum
from pydantic import BaseModel
from typing import Dict, Set, List


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
    id: str


class DeckCreate(DeckBase):
    pass


class Deck(DeckBase):
    pass


class CardBase(BaseModel):
    deck_id: str
    type: CardType
    text: str

    class Config:
        orm_mode = True


class CardCreate(CardBase):
    pass


class Card(CardBase):
    id: int

    def __hash__(self):
        return hash(self.id)


class PlayerState(int, Enum):
    not_ready = 0
    ready = 1
    waiting = 2
    complete = 3


class PlayerType(str, Enum):
    child = "child"
    changeling = "changeling"


class GameBase(BaseModel):
    id: str
    changeling_deck_id: str
    child_deck_id: str

    class Config:
        orm_mode = True


class GameCreate(GameBase):
    pass


class Game(GameBase):
    current_round: int = 1


class Hand(BaseModel):
    relationships: List[Card]
    possessions: List[Card]
    actions: List[Card]
    feelings: List[Card]


class RoundBase(BaseModel):
    round_number: int
    changeling_waiting: PlayerState = PlayerState.not_ready
    child_waiting: PlayerState = PlayerState.not_ready
    changeling_hand: Hand
    child_hand: Hand
    game_id: str


class RoundCreate(RoundBase):
    pass


class Round(RoundBase):
    id: int
