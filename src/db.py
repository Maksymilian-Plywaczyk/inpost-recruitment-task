from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy_utils import database_exists

engine = create_engine(
    "sqlite:///database.db", connect_args={"check_same_thread": False}
)  # Here we create database in our memory, obviously you can name it whatever you like

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@as_declarative()
class Base:
    def _asdict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}


def create_db_and_tables():
    Base.metadata.create_all(engine)


def get_db() -> Session:
    db = SessionLocal()
    return db


def is_database_exists() -> bool:
    if database_exists(engine.url):
        return True
    return False
