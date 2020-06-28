from sqlalchemy import Table, Column, String, Integer, ForeignKey
from .database import metadata

users = Table(
    "users",
    metadata,
    Column('user_id', String(8), primary_key=True),
    Column('email', String),
    Column("secret_question", String),
    Column('password', String),
    Column("secret_answer", String)
)