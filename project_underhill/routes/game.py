from fastapi import APIRouter, status, Request, Form
from fastapi.templating import Jinja2Templates
from ..core import crud, schema
from ..core.security import get_random_string
from typing import List, Optional

import asyncio

router = APIRouter()
templates = Jinja2Templates(directory="project_underhill/templates")


@router.get("/start")
async def create_game(request: Request):

    return templates.TemplateResponse("create_game.html", {"request": request})


@router.post("/setup")
async def setup_game(changeling=Form(None), child=Form(None)):

    strings = (process_string(changeling), process_string(child))

    return {"changeling": strings[0], "child": strings[1]}


def process_string(string: str) -> str:
    if "/" in string:
        string = string.split("/")[-1]
    return string
