from sqlmodel import Session
from config.DatabaseConfig import engine

def get_session():
    with Session(engine) as session:
        yield session
