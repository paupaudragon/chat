from sqlmodel import Session, SQLModel, create_engine, select
from datetime import datetime
from fastapi import HTTPException

from backend.schema import (
    UserChatLinkInDB, 
    UserInDB,
    ChatInDB,
    ChatUpdate,
    Chat,
    User,
    Message,
    ChatResponse,
    ChatMetadata,
    ChatResponse_Message,
    ChatResponse_User,
    ChatResponse_Both,
    Text,
    MessageInDB,
    ChatCreateResponse,
    UserCollection,
    Metadata
)

engine = create_engine(
    "sqlite:///backend/pony_express.db/sample.db",
    echo=True,
    connect_args={"check_same_thread": False},
)

class AuthException(HTTPException):##inherit from HTTPException
    def __init__(self, error: str, description: str, status_code: int):
        super().__init__(
            status_code=status_code,
            detail={
                "error": error,
                "error_description": description,
            },
        )


class NoPermission(AuthException):
    def __init__(self):
        super().__init__(
            status_code = 403,
            error="no_permission",
            description="requires permission to edit chat members",
        )

class NoPermission_2(AuthException):
    def __init__(self):
        super().__init__(
            status_code = 403,
            error="no_permission",
            description="requires permission to edit chat",
        )


class DeleteOwner(AuthException):
    def __init__(self):
        super().__init__(
            status_code=422,
            error="invalid_state",
            description="owner of the chat cannot be removed",
        )

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
    

class DuplicateEntityException(Exception):
    def __init__(self, *, entity_name: str, entity_id: str):
        self.entity_name = entity_name
        self.entity_id = entity_id


class EntityNotFoundException(Exception):
    def __init__(self, *, entity_name: str, entity_id: str):
        self.entity_name = entity_name
        self.entity_id = entity_id

def get_all_users(session: Session) -> list[UserInDB]:
    """
    Retrieve all users from the database.

    :return: ordered list of users
    """
    return session.exec(select(UserInDB)).all()


def create_user(session: Session,user_create: UserInDB) -> UserInDB:
    """
    Create a new user in the database.

    :param user_create: attributes of the user to be created
    :return: the newly created user
    """
    user = UserInDB(**user_create.model_dump())
    session.add(user)
    session.commit()
    session.refresh(user)
    return user



def get_user_by_id(session: Session, user_id: int) -> UserInDB:
    """
    Retrieve an user from the database.

    :param user_id: id of the user to be retrieved
    :return: the retrieved user
    :raises EntityNotFoundException: if no such user id exists
    """
    user = session.get(UserInDB, user_id)
    if user:
        return user

    raise EntityNotFoundException(entity_name="User", entity_id=user_id)


###################### chats ######################
def get_all_chats(session:Session)->list[Chat]:
    """
    Retrieve all users from the database.

    :return: ordered list of users
    """
    stmt = select(ChatInDB)

    # Execute the statement and fetch all results
    results = session.exec(stmt).all()    
    list = []
    for chat in results:
        list.append(
            Chat(
                id = chat.id,
                name = chat.name,
                owner = User(**chat.owner.model_dump()),
                created_at=chat.created_at
            )
        )
    return list

def get_chat_by_id(session:Session, 
                   chat_id: str,
                   include : list[str],
                   ):
    """   
    Retrieve a chat from the database.

    :param chat_id: id of the chat to be retrieved
    :return: the retrieved chat
    :raises EntityNotFoundException: if no such animal id exists
    """
    chat = session.get(ChatInDB, chat_id)

    if not chat:
        raise EntityNotFoundException(entity_name="Chat", entity_id=chat_id)

    chat_meta = ChatMetadata(
        message_count=len(chat.messages),
        user_count=len(chat.users)
    )

    chat_res = Chat(
        id=chat.id,
        name=chat.name,
        owner=User(**chat.owner.model_dump(exclude_none=True)),
        created_at=chat.created_at
    )
    if include is None: 
        return ChatResponse(meta=chat_meta, chat=chat_res)
    
    users =[]
    messages =[]
    if 'users' in include:
        users = [User(**user.model_dump(exclude_none=True)) for user in chat.users]
        if len(include) ==1: 
            return ChatResponse_User(meta=chat_meta, chat=chat_res, users=users)
    
    if 'messages' in include:
        messages = [
            Message(
                id=m.id,
                text=m.text,
                chat_id=m.chat_id,
                user=User(**m.user.model_dump(exclude_none=True)),
                created_at=m.created_at
            ) for m in chat.messages
        ]
        if len(include) ==1: 
            return ChatResponse_Message(meta=chat_meta, chat=chat_res, messages=messages)
    
    return ChatResponse_Both(meta=chat_meta, chat=chat_res, messages = messages, users=users)
#################################################################################################
################################################################################################
def update_chat(session:Session, 
                chat_id: str, 
                chat_update: ChatUpdate, 
                user) -> ChatInDB:
    """
    Update a chat in the database.

    :param chat_id: id of the animal to be updated
    :param chat_update: attributes to be updated on the chat
    :return: the updated chat
    :raises EntityNotFoundException: if no such chat id exists
    """

    chat = get_chat_by_id_helper(session, chat_id)

    if chat.owner_id != user.id:
        raise NoPermission_2()
    
    print("same personnnnnnnnnnnnnnnnnnn")

    for attr, value in chat_update.model_dump(exclude_none=True).items():
        setattr(chat, attr, value)


    session.add(chat)
    session.commit()
    session.refresh(chat)
    return chat

def get_chat_by_id_helper(session:Session, chat_id) -> ChatInDB:
    chat = session.get(ChatInDB, chat_id)
    if chat: 
        return chat
    raise EntityNotFoundException(entity_name="Chat", entity_id=chat_id)
    
    
def get_chat_messages(session:Session, chat_id : int)->list[Message]:

    chat = get_chat_by_id_helper(session, chat_id); 

    msg_list = []
    messages = chat.messages; 
    for msg_in_db in messages:
        message = Message(
            chat_id= msg_in_db.chat_id,
            created_at= msg_in_db.created_at,
            id= msg_in_db.id,
            text= msg_in_db.text,
            user_id= msg_in_db.user_id,
            user= User(**msg_in_db.user.model_dump()),
        )
        msg_list.append(message)
    return msg_list

def add_a_message(session: Session, 
                  chat_id: int, 
                  new_msg: Text, 
                  user: UserInDB
                  )->Message:
    
    chat = get_chat_by_id_helper(session, chat_id); 
    message = MessageInDB(
        text = new_msg.text, 
        user_id = user.id,
        chat_id = chat_id, 
        user = user
    )
    session.add(message)
    session.commit()
    session.refresh(message)
    # print(message)
    msg_res = Message(**message.model_dump(), 
                      user = User(**message.user.model_dump())
    )
    return msg_res

def get_chat_users(session:Session, chat_id : int)->list[User]:
    users = session.exec(select(UserInDB).join(ChatInDB.users).where(ChatInDB.id == chat_id)).all()
    print(users)
    user_list = []
    for u in users:
        user_list.append(User(**u.model_dump()))
    return user_list

def get_user_chats(session: Session, user_id: int) -> list[Chat]:
    """
    Retrieve chats associated with a user using a raw SQL query.

    :param session: SQLAlchemy database session
    :param user_id: ID of the user
    :return: List of Chat objects
    """
    results = session.exec(
        select (ChatInDB)
        .join(UserChatLinkInDB)
        .where(UserChatLinkInDB.user_id == user_id)
        .distinct(ChatInDB.id)
    ).all()

    print(results)

    # Convert results to Chat objects
    chat_list = []
    for chat_in_db in results:
        chat = Chat(
            id=chat_in_db.id,
            name=chat_in_db.name,
            owner=User(**chat_in_db.owner.model_dump()),
            created_at=chat_in_db.created_at
        )
        chat_list.append(chat)
    return chat_list

        

    
# def delete_chat(chat_id: str):
#     """
#     Delete an user from the database.

#     :param user_id: the id of the user to be deleted
#     """

#     chat = get_chat_by_id(chat_id)
#     del DB["chats"][chat.id]


def add_a_chat(session, chat_create, user)->ChatInDB:

    new_chat = ChatInDB(
        **chat_create.model_dump(), 
        owner_id = user.id
        )
    print("here")
    print(new_chat)
    session.add(new_chat)
    session.commit()
    session.refresh(new_chat)

    return new_chat

def add_user_to_chat(session, chat_id,user_id, owner)->UserCollection:
     
     #verify chat exist 
     chat = get_chat_by_id_helper(session, chat_id)

     #verify owner is the owner of the chat 
     if chat.owner_id != owner.id:
        raise NoPermission()
     
     user = session.get(UserInDB, user_id)
     if not user:
        raise EntityNotFoundException(entity_name="User", entity_id=user_id)
     
     if not session.query(UserChatLinkInDB).filter_by(chat_id=chat_id, user_id=user_id).first():
        chat.users.append(user)
        session.add(chat)
        session.commit()
        session.refresh(chat)

     return UserCollection(meta = Metadata(count = len(chat.users)), users= chat.users)

def delete_user_to_chat(session, chat_id,user_id, owner)->UserCollection:
     
     #verify chat exist 
     chat = get_chat_by_id_helper(session, chat_id)

     #verify owner is the owner of the chat 
     if chat.owner_id != owner.id:
        raise NoPermission()
     
     user = session.get(UserInDB, user_id)

     if not user:
        raise EntityNotFoundException(entity_name="User", entity_id=user_id)
     
     if user.id == chat.owner_id:
         raise DeleteOwner()
     
     if session.query(UserChatLinkInDB).filter_by(chat_id=chat_id, user_id=user_id).first():
        chat.users.remove(user)
        session.add(chat)
        session.commit()
        session.refresh(chat)

     return UserCollection(meta = Metadata(count = len(chat.users)), users= chat.users)
     

     
    

# def update_chat_name(session, chat_create, user, chat_id)->ChatInDB:
#     chat = get_chat_by_id_helper(session, chat_id); 
#     userid_in_chat = chat.owner_id
#     if userid_in_chat != user.id: 
#         return {
#             "detail": {
#                 "error": "no_permisson", 
#                 "error_description": "requires permission to edit chat"
#             }
#         }
    




