from fastapi import APIRouter, status, Request
from fastapi.templating import Jinja2Templates
from ..core import crud, schema
from typing import List

router = APIRouter()
templates = Jinja2Templates(directory="project_underhill/templates")


@router.get("/create")
async def create_user(request: Request):
    return templates.TemplateResponse("layout.html", {"request": request})


@router.get("/{deck_id}", response_model=List[schema.Card])
async def get_deck(deck_id: str):
    input_id = deck_id
    cards = await crud.get_cards_by_user(input_id)
    return cards
