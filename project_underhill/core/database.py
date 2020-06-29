import sqlalchemy
from sqlalchemy import MetaData, create_engine
import databases

DATABASE_URL = "sqlite:///./db.sqlite"

database = databases.Database(DATABASE_URL)

metadata = MetaData()

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
