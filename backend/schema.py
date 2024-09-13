from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from sqlmodel import Field, Relationship, SQLModel



class UserChatLinkInDB(SQLModel, table=True):
    """Database model for many-to-many relation of users to chats."""

    __tablename__ = "user_chat_links"

    user_id: int = Field(foreign_key="users.id", primary_key=True)
    chat_id: int = Field(foreign_key="chats.id", primary_key=True)


class UserInDB(SQLModel, table=True):
    """Database model for user."""

    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True)
    hashed_password: str
    created_at: Optional[datetime] = Field(default_factory=datetime.now)

    chats: list["ChatInDB"] = Relationship(
        back_populates="users",
        link_model=UserChatLinkInDB,
    )


class ChatInDB(SQLModel, table=True):
    """Database model for chat."""

    __tablename__ = "chats"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    owner_id: int = Field(foreign_key="users.id")
    created_at: Optional[datetime] = Field(default_factory=datetime.now)

    owner: UserInDB = Relationship()
    users: list[UserInDB] = Relationship(
        back_populates="chats",
        link_model=UserChatLinkInDB,
    )
    messages: list["MessageInDB"] = Relationship(back_populates="chat")


class MessageInDB(SQLModel, table=True):
    """Database model for message."""

    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    text: str
    user_id: int = Field(foreign_key="users.id")
    chat_id: int = Field(foreign_key="chats.id")
    created_at: Optional[datetime] = Field(default_factory=datetime.now)

    user: UserInDB = Relationship()
    chat: ChatInDB = Relationship(back_populates="messages")

#request model 
class UserCreate(SQLModel):
    username: str
    email:str
    password: str

class UserUpdate(BaseModel):
    username: str = None
    email: str = None

class ChatCreate(BaseModel):
    name: str
    
class ChatUpdate(BaseModel):
    name: str = None
    owner_id: int = None
    created_at: Optional[datetime] = None
    


#response model 
class User(SQLModel):
    id:int
    username:str
    email:str
    created_at: datetime
class UserResponse(BaseModel):
    user: User

class ChatUpdateResponse(BaseModel):
    id: int
    name: str
    owner:User
    created_at:datetime

class ChatCreateResponse(SQLModel):
    name: str
    owner:User
    created_at:datetime

class ChatResponseWrapper(BaseModel):
    chat: ChatUpdateResponse

class ChatMetadata(BaseModel):
    """Represnets the metadata for chat collections"""
    message_count: int
    user_count: int

class Chat(BaseModel):
    id:int
    name:str
    owner: User
    created_at: datetime

class NewChat(BaseModel):
    chat: Chat

class Message(BaseModel):
    id: int
    text: str
    chat_id: int
    user: User
    created_at: datetime
    
class MessageResponse(BaseModel):
    message: Message
class ChatResponse_User(BaseModel):
    meta:ChatMetadata
    chat:Chat
    users: list[User] = None

class ChatResponse_Message(BaseModel):
    meta:ChatMetadata
    chat:Chat
    messages : list[Message] = None

class ChatResponse_Both(BaseModel):
    meta:ChatMetadata
    chat:Chat
    messages : list[Message] = None
    users: list[User] = None


class ChatResponse(BaseModel):
    meta:ChatMetadata
    chat:Chat
class Metadata(BaseModel):
    """Represents metadata for a collection."""
    count: int
    
class MessageCollection(BaseModel):
    """Represents an API response for a collection of messages."""
    meta: Metadata
    messages: list[Message]  

class UserCollection(BaseModel): 
    """Represents an API response for a collection of users."""

    meta: Metadata
    users:list[User]

class ChatCollection(BaseModel):
    """Represents an API response for a collection of users."""
    meta: Metadata
    chats: list[Chat]

class Text(BaseModel):
    text: str






