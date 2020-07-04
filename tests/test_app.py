from project_underhill import __version__
from project_underhill.core.main import create_app
from project_underhill.core.database import database
from fastapi.testclient import TestClient
from lorem_text.lorem import words
from asyncio import run


client = TestClient(create_app())


def build_deck():
    url = "deck/create/add_to_db"
    data = {
        "r1": words(2),
        "r2": words(2),
        "r3": words(2),
        "r4": words(2),
        "r5": words(2),
        "p1": words(2),
        "p2": words(2),
        "p3": words(2),
        "p4": words(2),
        "p5": words(2),
        "a1": words(2),
        "a2": words(2),
        "a3": words(2),
        "a4": words(2),
        "a5": words(2),
        "f1": words(2),
        "f2": words(2),
        "f3": words(2),
        "f4": words(2),
        "f5": words(2),
    }

    response = client.post(url, data)
    return response


def test_version():
    assert __version__ == "0.1.0"


if __name__ == "__main__":

    build_deck()
    build_deck()
