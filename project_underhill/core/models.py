from sqlalchemy import Table, Column, String, Integer, ForeignKey, Enum
from .database import metadata, engine
from .schema import CardType

users = Table(
    "users",
    metadata,
    Column("id", String, primary_key=True),
    Column("email", String),
    Column("secret_question", String),
    Column("password", String),
    Column("secret_answer", String),
)

decks = Table(
    "decks",
    metadata,
    Column("id", String(8), primary_key=True),
    Column("owner_id", Integer, ForeignKey("users.id")),
)


cards = Table(
    "cards",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("deck_id", String(8), ForeignKey("decks.id"), nullable=False),
    Column("type", Enum(CardType)),
    Column("text", String),
)

