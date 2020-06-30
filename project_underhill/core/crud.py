from . import models
from . import schema
from .security import pwd_context, get_random_string
from .database import database
from sqlite3 import IntegrityError
from sqlalchemy import select
from typing import List


async def create_user(user: schema.UserCreate) -> schema.User:
    users = models.users
    user.password = pwd_context.hash(user.password)
    user.secret_answer = pwd_context.hash(user.secret_answer)
    user_id = await get_random_string()
    while True:
        try:
            query = users.insert().values(**user.dict(), id=user_id)

            await database.execute(query)
            break
        except IntegrityError:
            user_id = await get_random_string()

    query = users.select().where(users.c.id == user_id)
    user: schema.User = await database.fetch_one(query)
    return user


async def create_card(card: schema.CardCreate):
    cards = models.cards
    query = cards.insert().values(**card.dict())
    await database.execute(query)


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

    user_cards = [dict(card) for card in user_cards]

    return user_cards
