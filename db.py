from typing import Annotated
from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, Session, create_engine

sqlite_name = "db.sqlite3"
sqlilte_url = f"sqlite:///{sqlite_name}"


engine = create_engine(sqlilte_url)


def create_all_tables(app: FastAPI):
    """Create all tables in the database."""
    SQLModel.metadata.create_all(engine)
    yield


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
