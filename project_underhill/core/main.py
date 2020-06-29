from fastapi import FastAPI

from . import schema
from . import models
from .database import database

app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/")
async def root():
    return {"message":"ok"}

@app.post("/user", response_model= schema.User)
async def create_user(user: schema.UserCreate):
    query = models.users.insert().values(email= user.email, password=user.password, id = "userID")
    last_record_id = await  database.execute(query)
    return {**user.dict(), "id" : last_record_id}
