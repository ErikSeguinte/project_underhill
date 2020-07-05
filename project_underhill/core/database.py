import sqlalchemy
from sqlalchemy import MetaData, create_engine
import databases
import ssl

from dotenv import load_dotenv
from os import getenv

load_dotenv()

DATABASE_URL = getenv("DATABASE_URL")
ctx = ssl.create_default_context(cafile="")
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

database = databases.Database(DATABASE_URL, ssl=ctx, max_size=5, min_size=3)

metadata = MetaData()

engine = create_engine(DATABASE_URL)
