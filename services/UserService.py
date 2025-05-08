import logging
from sqlmodel import Session
from exception import UserNotFoundException
from models.User import User
from schemas.User import UserRequest, UserResponse
from repositories import UserRepo

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 

def add_user(session: Session, request: UserRequest) -> UserResponse:
    user = User(**request.model_dump())
    saved = UserRepo.create_user(session, user)
    return UserResponse.model_validate(saved.__dict__)

def list_users(session: Session) -> list[UserResponse]:
    users = UserRepo.get_all_users(session)
    return [UserResponse.model_validate(user.model_dump()) for user in users]

def get_user_by_id(session: Session, user_id: int) -> UserResponse:
    user = UserRepo.get_user(session, user_id)
    if not user:
        logger.info(f"User not fount: {user_id}")
        raise UserNotFoundException()
    return UserResponse.model_validate(user.__dict__)

def update_user(session: Session, user_id: int, data: UserRequest) -> UserResponse:
    user = UserRepo.get_user(session, user_id)
    if not user:
        logger.info(f"User not fount: {user_id}")
        raise UserNotFoundException()
    
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(user, key, value)

    updated_user = UserRepo.create_user(session, user)
    return UserResponse.model_validate(updated_user.model_dump())

def delete_user(session: Session, user_id: int):
    user = UserRepo.get_user(session, user_id)
    if not user:
        logger.info(f"User not fount: {user_id}")
        raise UserNotFoundException()
    
    UserRepo.delete_user(session, user)