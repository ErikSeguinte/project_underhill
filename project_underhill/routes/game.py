from fastapi import APIRouter, status, Request, Form
from fastapi.templating import Jinja2Templates
from ..core import crud, schema, models
from typing import List, Optional

import asyncio

router = APIRouter()
templates = Jinja2Templates(directory="project_underhill/templates")


@router.get("/start")
async def create_game(request: Request):

    return templates.TemplateResponse("create_game.html", {"request": request})


@router.post("/setup")
async def setup_game(changeling=Form(None), child=Form(None)):

    id = await crud.get_unique_string(models.games)
    child = process_string(child)
    changeling = process_string(changeling)
    game: schema.GameCreate = schema.GameCreate(
        id=id, child_deck_id=child, changeling_deck_id=changeling,
    )

    aws = [
        crud.create_game(game),
        crud.get_cards_by_deck(changeling),
        crud.get_cards_by_deck(child),
    ]

    results = await asyncio.gather(*aws)

    return {"results": results[1], "results2": results[2]}


async def setup_round_one(id, changeling_cards, child_cards):
    pass


def process_string(string: str) -> str:
    if "/" in string:
        string = string.split("/")[-1]
    return string
