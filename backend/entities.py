from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

################### Metadata ########################

################### User ########################
class UserInDB(BaseModel):
    """Represents a user in database."""

    id: str
    created_at: datetime

class UserCreate(BaseModel):
    """ Represents paramers  for adding a new user to the system. """

    id: str = None

class UserResponse(BaseModel):
    user: UserInDB

################### Chat ########################
class ChatInDB (BaseModel):
    """Represents a chat in database."""
    id: str
    name: str
    user_ids: list[str]
    owner_id: str
    created_at: datetime 

class ChatResponse(BaseModel):
    """Represents an API response for a chat."""

    chat: ChatInDB

################## Message ################
    
class MessageInDB(BaseModel):
    """Represents a message in database."""

    id: str
    user_id: str
    text: str
    created_at: datetime

 


#Request model 

class ChatUpdate(BaseModel):

    id:str= None
    name: str = None
    user_ids: list[str] = None
    owner_id: str= None
    created_at: datetime= None


#response model 
    
class Metadata(BaseModel):
    """Represents metadata for a collection."""

    count: int
    
class UserCollection(BaseModel): 
    """Represents an API response for a collection of users."""

    meta: Metadata
    users:list[UserInDB]
    
class ChatCollection(BaseModel):
    """Represents an API response for a collection of users."""

    meta: Metadata
    chats: list[ChatInDB]  

class MessageCollection(BaseModel):
    """Represents an API response for a collection of messages."""

    meta: Metadata
    messages: list[MessageInDB]  