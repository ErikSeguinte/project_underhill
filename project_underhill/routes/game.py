from fastapi import APIRouter, status, Request, Form
from fastapi.templating import Jinja2Templates
from ..core import crud, schema, models
from typing import List, Optional
from random import choices

import asyncio

router = APIRouter()
templates = Jinja2Templates(directory="project_underhill/templates")


@router.get("/start")
async def create_game(request: Request):

    return templates.TemplateResponse("create_game.html", {"request": request})


@router.post("/setup")
async def setup_game(changeling=Form(None), child=Form(None)):

    task = asyncio.create_task(crud.get_unique_string(models.games))
    child = process_string(child)
    changeling = process_string(changeling)
    id = await task
    game: schema.GameCreate = schema.GameCreate(
        id=id, child_deck_id=child, changeling_deck_id=changeling,
    )

    aws = [
        crud.create_game(game),
        crud.get_cards_by_deck(changeling),
        crud.get_cards_by_deck(child),
    ]

    results = await asyncio.gather(*aws)

    combined_deck = categorize_decks(results[1] + results[2])
    setup_round_one(id, combined_deck)

    return {"results": results[1], "results2": results[2]}


def categorize_decks(cards):
    processed_cards = {}
    for card in cards:
        if processed_cards.get(card.type):
            processed_cards[card.type].append(card)
        else:
            processed_cards[card.type] = [card]

    return processed_cards


def deal_cards(cards):
    changeling = {}
    child = {}

    for card_type in schema.CardType.__members__:
        superset = set(choices(cards[card_type], 10))
        changeling[card_type] = set(choices(superset, 5))
        child[card_type] = superset.difference(changeling)

    return changeling, child


async def setup_round_one(game_id, cards):
    await crud.create_round()


def process_string(string: str) -> str:
    if "/" in string:
        string = string.split("/")[-1]
    return string
