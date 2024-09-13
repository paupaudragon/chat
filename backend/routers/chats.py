from typing import Literal

from fastapi import APIRouter, Depends, Query,status, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlmodel import Session
from backend.auth import get_current_user,AuthException
from backend.database import get_chat_by_id_helper



from backend.schema import (
    ChatUpdate,
    ChatCollection,
    MessageCollection,
    UserCollection,
    UserInDB,
    Text,
    MessageResponse,
    ChatResponseWrapper, 
    ChatUpdateResponse,
    ChatCreate,
    NewChat,
    Chat,
    User,
)

from backend import database as db

chat_router = APIRouter(prefix='/chats', tags=['Chats'])

@chat_router.get(
        "/", 
        response_model=ChatCollection,
        description="Get all chats."
        )
def get_chats(
    sort: Literal["name"] = 'name',
    session: Session = Depends(db.get_session)
):
    """Get a collection of chats."""

    sort_key = lambda chat: getattr(chat, sort)
    chats = db.get_all_chats(session) #List of chats

    return ChatCollection(
        meta={"count": len(chats)}, 
        chats=sorted(chats, key = sort_key),
    )

@chat_router.get(
        "/{chat_id}/messages", 
        response_model= MessageCollection,
        description="Get a collections of messages of a given chat id.")
def get_chat_messages(chat_id: int,
                      session: Session = Depends(db.get_session),
                      ):

    messages = db.get_chat_messages(session, chat_id)

    return MessageCollection(
        meta={"count": len(messages )}, 
        messages = messages
    )



@chat_router.get(
    "/{chat_id}",
    description="Get a chat for a given chat id.",
)
def get_chat(chat_id: int,
            #  include: Literal["messages", "users"] = None,
             include : list[str] = Query(default=None),
             session: Session = Depends(db.get_session),
             ):
    """Get a chat for a given id."""
    chat = db.get_chat_by_id(session, chat_id, include)
    return chat

@chat_router.put(
        "/{chat_id}", 
        status_code=200,
        description="Update a chat with some given fileds and values."
        )
def update_current_chat(
    chat_id: str, 
    chat_update: ChatUpdate, 
    user: UserInDB = Depends(get_current_user),
    session: Session = Depends(db.get_session)):
    """Update a chat for a given id."""
    chat=db.update_chat(session, chat_id, chat_update, user)
    chat_res =  ChatUpdateResponse(
        **chat.model_dump(),
        owner = chat.owner,
    )

    return ChatResponseWrapper(chat = chat_res)
    
        

@chat_router.post(
    "/{chat_id}/messages",
    response_model= MessageResponse, 
    status_code=201,
    description= "Add a new message to a chat. "
)
def add_message(
    chat_id: str, 
    new_msg: Text, 
    user: UserInDB = Depends(get_current_user),
    session: Session = Depends(db.get_session)):
    """Adds a new message to a chat. """

    # return {"sucess": "success"}
    message = db.add_a_message(session, chat_id, new_msg, user)

    return MessageResponse(message = message)


# @chat_router.delete(
#     "/{chat_id}",
#     status_code = 204,
#     response_model = None,
#     description="Delete a chat"
# )
# def delete_chat(chat_id: str) -> None:
#     db.delete_chat(chat_id)


@chat_router.get("/{chat_id}/users", 
                response_model=UserCollection,
                description="Get a collections of users of a given chat id.")
def get_chat_users(chat_id: int, 
                    session: Session = Depends(db.get_session),
                   ):

    users = db.get_chat_users(session, chat_id)

    return UserCollection(
        meta={"count": len(users)}, 
        users = users
    )

@chat_router.post(
                  "/", 
                  description= "Add a chat",
                  status_code=201)
def add_chat( 
            chat_create: ChatCreate, 
            user: UserInDB = Depends(get_current_user),
         
            session: Session = Depends(db.get_session), 

            ):
    """Get a chat for a given id."""
    chatIndb = db.add_a_chat(session, chat_create, user)

    chat = Chat(
        **chatIndb.model_dump(), 
        owner = user

    )

    return NewChat(chat = chat)

@chat_router.put(
        "/{chat_id}/users/{user_id}", 
        status_code=201,
        description= "Add a user to a chat")
def add_user_to_chat( 
            chat_id: int,
            user_id: int,
            owner: UserInDB = Depends(get_current_user),
            session: Session = Depends(db.get_session), 
            ):
    """Get a chat for a given id."""
    # UserCollection
    users = db. add_user_to_chat(session, chat_id,user_id, owner)
    return users

@chat_router.delete(
        "/{chat_id}/users/{user_id}", 
            status_code=200,
        description= "delete a user to a chat")
def delete_user_to_chat( 
            chat_id: int,
            user_id: int,
            owner: UserInDB = Depends(get_current_user),
            session: Session = Depends(db.get_session), 
            ):
    """Get a chat for a given id."""
    # UserCollection
    users = db. delete_user_to_chat(session, chat_id,user_id, owner)
    return users