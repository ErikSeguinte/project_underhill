from fastapi import FastAPI
from fastapi import status

from . import schema
from .database import database
from . import models
from . import crud

from .security import pwd_context, get_random_string

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/")
async def root():
    return {"message": "ok"}


@app.post("/user", response_model=schema.User, status_code=status.HTTP_201_CREATED)
async def create_user(user: schema.UserCreate):
    new_user = await crud.create_user(user)
    return new_user
