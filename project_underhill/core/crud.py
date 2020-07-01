from . import models
from . import schema
from .security import pwd_context, get_random_string
from .database import database
from sqlite3 import IntegrityError
from sqlalchemy import select
from typing import List, Dict, Union


async def create_user(user: schema.UserCreate) -> schema.User:
    users = models.users
    user.password = pwd_context.hash(user.password)
    user.secret_answer = pwd_context.hash(user.secret_answer)
    user_id = get_random_string()
    while True:
        try:
            query = users.insert().values(**user.dict(), id=user_id)

            await database.execute(query)
            break
        except IntegrityError:
            user_id = get_random_string()

    query = users.select().where(users.c.id == user_id)
    user: schema.User = await database.fetch_one(query)
    return schema.User.from_orm(user)


async def create_card(card: schema.CardCreate):
    cards = models.cards
    query = cards.insert().values(**card.dict())
    await database.execute(query)


async def create_deck(owner_id="test", deck_id=None) -> schema.Deck:
    decks = models.decks
    if not deck_id:
        deck_id = get_unique_string(decks)
    deck = {"id": deck_id, "owner_id": owner_id}
    q = decks.insert().values(**deck)
    await database.execute(q)

    q = decks.select().where(decks.c.id == deck_id)
    deck = await database.fetch_one(q)
    return deck


async def create_cards(cards: List[Dict]):
    query = models.cards.insert()
    await database.execute_many(query, cards)


async def get_user_by_id(user_id: str) -> schema.User:
    users = models.users
    query = users.select().where(users.c.id == user_id)
    user: schema.User = await database.fetch_one(query)
    return user


async def get_cards_by_user(user_id: str):
    cards = models.cards.alias("c")
    users = models.users.alias("u")
    decks = models.decks.alias("d")
    query = (
        select([cards.c.deck_id, cards.c.id, cards.c.text, cards.c.type])
        .select_from(cards.join(decks).join(users))
        .where(users.c.id == user_id)
    )

    user_cards = await database.fetch_all(query)

    user_cards = [schema.Card.from_orm(card) for card in user_cards]

    return user_cards


async def get_cards_by_deck(deck_id: str, categorize=False):
    cards = models.cards
    decks = models.decks

    q = (
        select([cards.c.deck_id, cards.c.id, cards.c.text, cards.c.type])
        .select_from(cards.join(decks))
        .where(decks.c.id == deck_id)
    )

    user_cards = await database.fetch_all(q)

    if categorize:
        processed_cards = {}
        for card in user_cards:
            card = schema.Card.from_orm(card)
            if processed_cards.get(card.type):
                processed_cards[card.type].append(card)
            else:
                processed_cards[card.type] = [card]

    else:
        processed_cards = [schema.Card.from_orm(card) for card in user_cards]

    return processed_cards


async def create_game(new_game: schema.GameCreate):
    games = models.games
    query = games.insert().values(new_game.dict())
    await database.execute(query)


async def get_unique_string(table):
    while True:
        string = get_random_string()
        query = select([table.c.id]).where(table.c.id == string)
        result = await database.fetch_one(query)
        if not result:
            break

    return string


async def create_round(round: schema.RoundCreate):
    rounds = models.rounds
    query = rounds.insert().values(**round.dict())
    result = await database.execute(query)


async def get_game(game_id: str) -> schema.Game:
    games = models.games
    query = games.select().where(games.c.id == game_id)
    game = await database.fetch_one(query)
    return schema.Game.from_orm(game)
