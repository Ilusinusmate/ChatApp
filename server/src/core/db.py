from contextlib import asynccontextmanager
from sqlmodel import create_engine, Session, SQLModel

from models import *
from core.settings import DATABASE_URL


engine = create_engine(DATABASE_URL)


async def get_session():
    with Session(engine) as session:
        try:
            yield session
        except Exception as e:
            session.rollback()
            raise e

def init_db():
    SQLModel.metadata.create_all(engine)