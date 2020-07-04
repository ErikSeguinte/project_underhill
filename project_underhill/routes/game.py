from fastapi import APIRouter, status, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from ..core import crud, schema, models, game_logic
from typing import List, Optional
from random import sample

import asyncio

router = APIRouter()
templates = Jinja2Templates(directory="project_underhill/templates")


@router.get("/start")
async def create_game(request: Request):
    return templates.TemplateResponse("create_game.html", {"request": request})


@router.post("/setup")
async def setup_game(request: Request, changeling=Form(None), child=Form(None)):
    task = asyncio.create_task(crud.get_unique_string(models.games))
    child = process_string(child)
    changeling = process_string(changeling)
    id = await task
    game: schema.Game = schema.Game(
        id=id, child_deck_id=child, changeling_deck_id=changeling, current_round=1
    )

    aws = [
        crud.create_game(game),
        crud.get_cards_by_deck(changeling),
        crud.get_cards_by_deck(child),
    ]

    results = await asyncio.gather(*aws)

    combined_deck = categorize_decks(results[1] + results[2])
    aws = [setup_round(id, n, combined_deck) for n in range(1, 5)]

    await asyncio.gather(*aws)

    return RedirectResponse(f"/game/{id}", status_code=status.HTTP_303_SEE_OTHER)


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
        superset = sample(cards[card_type], k=10)
        key = f"{card_type}s"
        changeling[key] = set(sample(superset, k=5))
        child[key] = set(superset).difference(changeling[key])

    return parse_hand(changeling), parse_hand(child)


def parse_hand(cards) -> schema.Hand:
    return schema.Hand(**cards)


async def setup_round(game_id, round_number, cards):
    changeling, child = deal_cards(cards)
    game_round = schema.RoundCreate(
        round_number=round_number,
        game_id=game_id,
        changeling_hand=changeling,
        child_hand=child,
    )
    await crud.create_round(game_round)


def process_string(string: str) -> str:
    if "/" in string:
        string = string.split("/")[-1]
    return string


@router.post("/{game_id}/play")
async def play(request: Request, game_id: str, who: schema.PlayerType):
    game_round = await crud.get_round_by_game_id(game_id)
    response = await game_logic.play(game_round, who)
    if response:
        if response == "ready":
            # TODO
            pass
            if who == schema.PlayerType.changeling:
                cards = game_round.changeling_hand.to_list()
            else:
                cards = game_round.child_hand.to_list()
            return templates.TemplateResponse(
                "ready_to_play.html",
                {"request": request, "cards": cards, "who": who, "game_id": game_id},
            )
        else:
            hand, number, flags, owner = response

            return templates.TemplateResponse(
                "choose.html",
                {
                    "request": request,
                    "hand": hand,
                    "number": number,
                    "flags": flags,
                    "game_id": game_id,
                    "owner": owner,
                },
            )

    return {"message": "Please wait for your partner"}


@router.post("/{game_id}/process")
async def receive_cards(
    request: Request,
    owner: schema.PlayerType,
    game_id: str,
    flags: int = 0,
    r1: int = Form(None),
    r2: int = Form(None),
    r3: int = Form(None),
    r4: int = Form(None),
    r0: int = Form(None),
    p1: int = Form(None),
    p2: int = Form(None),
    p3: int = Form(None),
    p4: int = Form(None),
    p0: int = Form(None),
    a1: int = Form(None),
    a2: int = Form(None),
    a3: int = Form(None),
    a4: int = Form(None),
    a0: int = Form(None),
    f1: int = Form(None),
    f2: int = Form(None),
    f3: int = Form(None),
    f4: int = Form(None),
    f0: int = Form(None),
):
    game_round = await crud.get_round_by_game_id(game_id)
    if owner == schema.PlayerType.changeling:
        hand = game_round.changeling_hand
    else:
        hand = game_round.child_hand
    # relationships = [x for x in [r1, r2, r3, r4, r5] if x]
    relationships = [
        hand.relationships[n] for n in [r0, r1, r2, r3, r4] if n is not None
    ]
    possessions = [hand.possessions[n] for n in [p0, p1, p2, p3, p4] if n is not None]
    actions = [hand.actions[n] for n in [a0, a1, a2, a3, a4] if n is not None]
    feelings = [hand.feelings[n] for n in [f0, f1, f2, f3, f4] if n is not None]

    new_hand = schema.Hand(
        relationships=relationships,
        possessions=possessions,
        actions=actions,
        feelings=feelings,
    )

    aws = [
        crud.update_flags(game_id, schema.GameState(flags)),
        crud.update_hand(game_id, new_hand, owner),
    ]

    await asyncio.gather(*aws)
    return RedirectResponse(
        url=f"/game/{game_id}", status_code=status.HTTP_303_SEE_OTHER
    )


@router.post("/{game_id}/complete")
async def complete_round(
    game_id: str, who: schema.PlayerType, complete: str = Form("")
):
    if complete:
        if who == schema.PlayerType.changeling:
            new_flag = schema.GameState.changeling_complete
        else:
            new_flag = schema.GameState.child_complete

        await crud.update_flags(game_id=game_id, new_flags=new_flag)

        round = await crud.get_round_by_game_id(game_id)
        f = round.state
        states = schema.GameState
        both_completed = states.changeling_complete | states.child_complete
        if f & both_completed == both_completed:
            await crud.next_round(game_id)

    return RedirectResponse(
        url=f"/game/{game_id}", status_code=status.HTTP_303_SEE_OTHER
    )


@router.get("/{game_id}")
async def serve_lobby(request: Request, game_id: str):
    game = await crud.get_game(game_id)

    return templates.TemplateResponse("lobby.html", {"request": request, "game": game})
