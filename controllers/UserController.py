from fastapi import APIRouter, Depends, status, Response
from sqlmodel import Session
from config.Session import get_session
from services import UserService
from schemas.User import UserRequest, UserResponse
from typing import List

router = APIRouter()

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserRequest, session: Session = Depends(get_session)):
    return UserService.add_user(session, user)

@router.get("/", response_model=List[UserResponse])
def list_users(session: Session = Depends(get_session)):
    return UserService.list_users(session)

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, session: Session = Depends(get_session)):
    return UserService.get_user_by_id(session, user_id)

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_data: UserRequest, session: Session = Depends(get_session)):
    return UserService.update_user(session, user_id, user_data)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    UserService.delete_user(session, user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
