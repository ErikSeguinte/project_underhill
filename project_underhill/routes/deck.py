from fastapi import APIRouter, status, Request, Form, Response
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from ..core import crud, schema, models
from ..core.security import get_random_string
from typing import List, Optional
import asyncio

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
    request: Request,
    owner_id: str = "test",
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

    awaitables = []
    if not deck_id:
        deck_id = await crud.insure_unique(models.decks)
        awaitables.append(crud.create_deck(deck_id=deck_id))

    # Grab all the form data and put them into lists, ignoring blanks
    relationships = [x for x in [r1, r2, r3, r4, r5] if x]
    possessions = [x for x in [p1, p2, p3, p4, p5] if x]
    actions = [x for x in [a1, a2, a3, a4, a5] if x]
    feelings = [x for x in [f1, f2, f3, f4, f5] if x]

    things = []
    things += process_things(relationships, deck_id, schema.CardType.relationship)
    things += process_things(possessions, deck_id, schema.CardType.possession)
    things += process_things(actions, deck_id, schema.CardType.action)
    things += process_things(feelings, deck_id, schema.CardType.feeling)

    awaitables.append(crud.create_cards(things))
    results = await asyncio.gather(*awaitables)

    return RedirectResponse(
        url=f"/deck/{deck_id}", status_code=status.HTTP_303_SEE_OTHER
    )


def process_things(things: List, deck_id: str, card_type: schema.CardType):
    """turns a list of things into a list of dicts of things"""

    thing_list = [
        {"deck_id": deck_id, "type": card_type, "text": thing} for thing in things
    ]
    return thing_list


@router.get("/{deck_id}")
async def get_deck(deck_id: str, request: Request):
    cards = await crud.get_cards_by_deck(deck_id)
    return templates.TemplateResponse(
        "deck_info.html", {"request": request, "cards": cards, "deck_id": deck_id}
    )
