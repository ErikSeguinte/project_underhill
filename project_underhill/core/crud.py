from . import models
from . import schema
from .security import pwd_context, get_random_string
from .database import database
from sqlite3 import IntegrityError
from sqlalchemy import select


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
