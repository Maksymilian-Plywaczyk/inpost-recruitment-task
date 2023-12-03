from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

engine = create_engine(
    "sqlite:///database.db", connect_args={"check_same_thread": False}
)  # Here we create database in our memory, obviously you can name it whatever you like

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def create_db_and_tables():
    Base.metadata.create_all(engine)


def get_db() -> Session:
    db = SessionLocal()
    return db
