from enum import Enum, IntFlag, auto
from pydantic import BaseModel
from pprint import pprint

# noinspection PyPackageRequirements
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


class GameState(IntFlag):
    not_ready = 0
    changeling_self_cards_chosen = auto()
    changeling_other_cards_chosen = auto()
    child_self_cards_chosen = auto()
    child_other_cards_chosen = auto()
    changeling_complete = auto()
    child_complete = auto()


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

    def pprint(self):
        pprint([card.json() for card in self.relationships])
        pprint([card.json() for card in self.possessions])
        pprint([card.json() for card in self.actions])
        pprint([card.json() for card in self.feelings])

    def to_list(self):
        return self.relationships + self.possessions + self.actions + self.feelings


class RoundBase(BaseModel):
    round_number: int
    state: GameState = GameState(0)
    game_id: str
    changeling_hand: Hand
    child_hand: Hand

    class Config:
        orm_mode = True


class RoundCreate(RoundBase):
    pass


class Round(RoundBase):
    id: int
