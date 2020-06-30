from fastapi import APIRouter, status, Request, Form
from fastapi.templating import Jinja2Templates
from ..core import crud, schema
from ..core.security import get_random_string
from typing import List, Optional

router = APIRouter()
templates = Jinja2Templates(directory="project_underhill/templates")


@router.get("/create")
async def create_user(request: Request, deck_id: Optional[str] = None):

    labels = []
    for type in schema.CardType.__members__:
        for n in range(1, 6):
            label = [f"{type} {n}", f"{type[0]}{n}"]
            labels.append(label)

    return templates.TemplateResponse(
        "create_deck.html", {"request": request, "labels": labels, "deck_id": deck_id}
    )


@router.post("/create/add_to_db", status_code=status.HTTP_201_CREATED)
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
    deck_id: Optional[str] = None,
):
    relationships = [r1, r2, r3, r4, r5]
    possessions = [p1, p2, p3, p4, p5]
    actions = [a1, a2, a3, a4, a5]
    feelings = [f1, f2, f3, f4, f5]

    if not deck_id:
        deck_id = await get_random_string()

    await process_things(relationships, deck_id, schema.CardType.relationship)
    await process_things(possessions, deck_id, schema.CardType.possession)
    await process_things(actions, deck_id, schema.CardType.action)
    await process_things(feelings, deck_id, schema.CardType.feeling)

    return [deck_id, relationships, possessions, actions, feelings]


async def process_things(things: List, deck_id: str, type: schema.CardType):
    for thing in things:
        if thing:
            t = {"deck_id": deck_id, "type": type, "text": thing}

            await crud.create_card(schema.CardCreate(**t))


@router.get("/", response_model=List[schema.Card])
async def get_deck(deck_id: str):
    input_id = deck_id
    cards = await crud.get_cards_by_deck(input_id)
    return cards
