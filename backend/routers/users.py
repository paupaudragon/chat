from typing import Literal

from fastapi import APIRouter, Depends
from sqlmodel import Session

from backend.auth import get_current_user

from backend.schema import (
    UserCollection,
    UserResponse,
    ChatCollection,
    ChatResponse,
    UserCreate,
    UserInDB,
    UserUpdate
)
from backend import database as db

user_router = APIRouter(prefix='/users', tags=['Users'])

@user_router.get(
        "/", 
        response_model= UserCollection,
        description="Get all users and sort them by id.")
def get_users(
    sort: Literal["id"] = 'id',
    session: Session = Depends(db.get_session)
):
    """Get a collection of usera."""

    sort_key = lambda user: getattr(user, sort)
    users = db.get_all_users(session)

    return UserCollection(
        meta={"count": len(users)}, 
        users=sorted(users, key = sort_key),
    )

@user_router.get("/me", response_model=UserResponse)
def get_self(user: UserInDB = Depends(get_current_user)):
    """Get current user."""
    return UserResponse(user=user)

@user_router.post(
        "/", 
        response_model=UserResponse,
        description="Create a new user by providing a new id")
def create_user(user_create:UserCreate):
     """Add a new animal to the buddy system."""

     user = db.create_user(user_create)
     return UserResponse(user=user)

@user_router.put(
        "/me", 
        response_model = UserResponse
        )
def update_self(
    user_update: UserUpdate,
    user: UserInDB = Depends(get_current_user),
    session: Session = Depends(db.get_session)
    ):
    """Update a logged in user's username or email."""
    if user_update.username: 
        user.username = user_update.username
    if user_update.email: 
        user.email = user_update.email 

    session.add(user)
    session.commit()
    session.refresh(user)

    return UserResponse(user=user)
    

@user_router.get(
    "/{user_id}",
    response_model=UserResponse,
    description="Get an user for a given user id.",
)
    
def get_user(user_id: int,
             session: Session = Depends(db.get_session),
             ):
    """Get an user for a given id."""

    user = db.get_user_by_id(session, user_id)
    return UserResponse(user = user)


@user_router.get(
        "/{user_id}/chats", 
        response_model=ChatCollection,
        description="Get a collection of chats a user participates.")
def get_user_chats(user_id: int,
                   session: Session = Depends(db.get_session),
                   ):
    print("user id:" + str(user_id))
    chats = db.get_user_chats(session, user_id) #List of chats

    return ChatCollection(
        meta={"count": len(chats)}, 
        chats=chats,
    )