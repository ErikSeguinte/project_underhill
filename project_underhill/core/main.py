from fastapi import FastAPI
from .database import database
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .security import pwd_context, get_random_string
from ..routes.deck import router as deck_router
from ..routes.game import router as game_router

app = FastAPI()

app.include_router(deck_router, prefix="/deck")
app.include_router(game_router, prefix="/game")

app.mount("/static", StaticFiles(directory="project_underhill/static"), name="static")


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/")
async def root():
    return {"message": "ok"}
