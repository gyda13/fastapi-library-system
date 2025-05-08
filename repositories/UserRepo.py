from sqlmodel import Session, select
from models.User import User
from typing import List, Optional

def create_user(session: Session, user: User) -> User:
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def get_user(session: Session, user_id: int) -> Optional[User]:
    return session.get(User, user_id)

def get_all_users(session: Session) -> List[User]:
    return session.exec(select(User)).all()


def delete_user(session: Session, user: User):
    session.delete(user)
    session.commit()