from fastapi import APIRouter, status
from fastapi.templating import Jinja2Templates
from ..core import crud, schema
from typing import List

router = APIRouter()
templates = Jinja2Templates(directory="../templates")


@router.get("/create")
async def create_user(user: schema.UserCreate):
    new_user = await crud.create_user(user)
    return templates.TemplateResponse("layout.html", {})


@router.get("/{deck_id}", response_model=List[schema.Card])
async def get_deck(deck_id: str):
    input_id = deck_id
    cards = await crud.get_cards_by_user(input_id)
    return cards
