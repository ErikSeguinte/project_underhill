from fastapi import APIRouter, status, Request, Form
from fastapi.templating import Jinja2Templates
from ..core import crud, schema
from typing import List

router = APIRouter()
templates = Jinja2Templates(directory="project_underhill/templates")


@router.get("/create")
async def create_user(request: Request):

    labels = []
    for type in schema.CardType.__members__:
        for n in range(1, 6):
            label = [f"{type} {n}", f"{type[0]}{n}"]
            labels.append(label)

    return templates.TemplateResponse(
        "create_deck.html", {"request": request, "labels": labels}
    )


@router.post("/create/add_to_db")
async def receive_cards(
    r1: str = Form(""),
    r2: str = Form(""),
    r3: str = Form(""),
    r4: str = Form(""),
    r5: str = Form(""),
    p1: str = Form(""),
    p2: str = Form(""),
    p3: str = Form(""),
    p4: str = Form(""),
    p5: str = Form(""),
    a1: str = Form(""),
    a2: str = Form(""),
    a3: str = Form(""),
    a4: str = Form(""),
    a5: str = Form(""),
    f1: str = Form(""),
    f2: str = Form(""),
    f3: str = Form(""),
    f4: str = Form(""),
    f5: str = Form(""),
):
    relationships = [r1, r2, r3, r4, r5]
    possessions = [p1, p2, p3, p4, p5]
    actions = [a1, a2, a3, a4, a5]
    feelings = [f1, f2, f3, f4, f5]

    return [relationships, possessions, actions, feelings]


@router.get("/{deck_id}", response_model=List[schema.Card])
async def get_deck(deck_id: str):
    input_id = deck_id
    cards = await crud.get_cards_by_user(input_id)
    return cards
