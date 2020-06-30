from fastapi import APIRouter, status, Request, Form
from fastapi.templating import Jinja2Templates
from ..core import crud, schema
from ..core.security import get_random_string
from typing import List, Optional

router = APIRouter()
templates = Jinja2Templates(directory="project_underhill/templates")


@router.get("/start")
async def create_game(request: Request, deck_id: Optional[str] = None):

    labels = []
    for type in schema.CardType.__members__:
        for n in range(1, 6):
            label = [f"{type} {n}", f"{type[0]}{n}"]
            labels.append(label)

    return templates.TemplateResponse(
        "create_deck.html", {"request": request, "labels": labels, "deck_id": deck_id}
    )


@router.post("/create/add_to_db", status_code=status.HTTP_201_CREATED)
async def receive_cards():
    pass


async def process_things(things: List, deck_id: str, type: schema.CardType):
    for thing in things:
        if thing:
            t = {"deck_id": deck_id, "type": type, "text": thing}

            await crud.create_card(schema.CardCreate(**t))


@router.get("/{deck_id}", response_model=List[schema.Card])
async def get_deck(deck_id: str):
    input_id = deck_id
    cards = await crud.get_cards_by_user(input_id)
    return cards
