import pytest
from datetime import datetime

from backend.main import app
from backend.schema import ChatInDB,UserInDB,MessageInDB


@pytest.fixture
def default_users():
    return[
        UserInDB(
            id = 1, 
            username= "a",
            email="a@mail.com",
            hashed_password= "123",
            created_at=datetime(2019, 8, 15, 2, 13, 58)
        ),
         UserInDB(
            id = 2, 
            username= "b",
            email="b@mail.com",
            hashed_password= "123",
            created_at=datetime(2019, 9, 15, 2, 13, 58)
        ),
         UserInDB(
            id = 1, 
            username= "c",
            email="c@mail.com",
            hashed_password= "123",
            created_at=datetime(2019, 10, 15, 2, 13, 58)
        )
    ]

@pytest.fixture
def default_chats():
    return [
        ChatInDB(
            id=1,
            name="skynet",
            owner_id = 1,
            created_at = datetime(2019, 10, 15, 2, 13, 58)
            # users = [
            #     default_users[0], default_users[1]
            # ],
            # messages = [default_messages[0], default_messages[1]]
        ),
        ChatInDB(
            id=2,
            name= "start",
            owner_id = 0,
            created_at = datetime(2019, 10, 15, 2, 13, 58)

            # users = [
            #     default_users[0], default_users[1], default_users[2]
            # ],
            # messages = [default_messages[2], default_messages[3],  default_messages[4]]
            
        ),
        ChatInDB(
            id=3,
            name="bagels",
            owner_id = 2,
            created_at = datetime(2019, 10, 15, 2, 13, 58)
            # users = [
            #     default_users[1], default_users[2]
            # ],
            # messages = [default_messages[5], default_messages[6]]
        ),
    ]

@pytest.fixture
def default_messages():
    return [
        MessageInDB(
            id = 1, 
            text = "Hi this is a.", 
            user_id = 1, 
            chat_id = 1, 
            created_at = datetime(2019, 9, 15, 2, 14, 50)
        ),
        MessageInDB(
            id = 2, 
            text = "Hi this is b.", 
            user_id = 2, 
            chat_id = 1, 
            created_at = datetime(2019, 9, 15, 2, 15, 50)
        ),
        MessageInDB(
            id = 3, 
            text = "Hi this is a.", 
            user_id = 1, 
            chat_id = 2, 
            created_at = datetime(2019, 9, 15, 2, 14, 50)
        ),
        MessageInDB(
            id = 4, 
            text = "Hi this is b.", 
            user_id = 2, 
            chat_id = 2, 
            created_at = datetime(2019, 9, 15, 2, 15, 50)
        ),
        MessageInDB(
            id = 5, 
            text = "Hi this is c.", 
            user_id = 3, 
            chat_id = 2, 
            created_at = datetime(2019, 9, 15, 2, 16, 50)
        ),
           MessageInDB(
            id = 6, 
            text = "Hi this is b.", 
            user_id = 2, 
            chat_id = 3, 
            created_at = datetime(2019, 9, 15, 2, 22, 50)
        ),
        MessageInDB(
            id = 7, 
            text = "Hi this is c.", 
            user_id = 3, 
            chat_id = 3, 
            created_at = datetime(2019, 9, 15, 2, 23, 50)
        ),
    ]



#################### Get all chats ####################
def test_get_all_chats(client):
    response = client.get("/chats")
    assert response.status_code == 200

    meta = response.json()["meta"]
    chats = response.json()["chats"]
    assert meta["count"] == len(chats)
    assert chats == sorted(chats, key=lambda chat: chat["name"])

def test_get_all_chats_sorted_by_id(client):
    response = client.get("/chats?sort=id")
    assert response.status_code == 422
    assert response.json()['detail'][0]['type'] == "literal_error"

    

def test_get_all_chats_sorted_by_non_exsit_attr(client):
    response = client.get("/users?sort=email")
    assert response.status_code == 422
    assert response.json()['detail'][0]['type'] == "literal_error"
    

#################### Get a Chat by id ####################
def test_get_chat_valid_id(client, default_chats, session):
    db_chat = default_chats
    session.add_all(db_chat)

    chat_id = "1"
    response = client.get(f"/chats/{chat_id}")
    print(response)
    assert response.status_code == 200
    jsn_str =  response.json()
    assert jsn_str["chat"]['name'] == 'skynet'
    # assert jsn_str['chat']['owner_id'] == 1

def test_get_chat_invalid_id(client):
    chat_id = "z"
    response = client.get(f"/chats/{chat_id}")
    assert response.status_code == 404
    assert response.json() == {
        "detail": {
            "type": "entity_not_found",
            "entity_name": "Chat",
            "entity_id": chat_id,
        },
    }

    ################### Update a chat ###################
def test_update_chat_name(client):
    chat_id = "6215e6864e884132baa01f7f972400e2"

    update_params = {"name":"updated name"}
    response = client.put(f"/chats/{chat_id}", json=update_params)
    # print(response.json())
    assert response.status_code == 200
    assert response.json()['chat']['name'] == update_params['name']

    # test that the update is persisted
    response = client.get(f"/chats/{chat_id}")
    # print("GET Response:", response.json())  
    assert response.status_code == 200
    assert response.json()["chat"]['name'] == update_params['name']


def test_update_chat_invalid_id(client):
    chat_id = "invalid_id"
    update_params = {
        "name": "updated name",
    }
    response = client.put(f"/chats/{chat_id}", json=update_params)
    assert response.status_code == 404
    assert response.json() == {
        "detail": {
            "type": "entity_not_found",
            "entity_name": "Chat",
            "entity_id": chat_id,
        },
    }

################# Get chat messages #####################
def test_get_chat_messages_valid_id(client):

    chat_id = "734eeb9ddaec43b2ab6e289a0d472376"  
    response = client.get(f"/chats/{chat_id}/messages")

    assert response.status_code == 200

    response_data = response.json()
    print (response_data)
    assert response_data['meta'] == {'count': 95}

    ##################################################
    chat_id = "660c7a6bc1324e4488cafabc59529c93"  
    response = client.get(f"/chats/{chat_id}/messages")

    assert response.status_code == 200

    response_data = response.json()
    print (response_data)
    assert response_data['meta'] == {'count': 19} 

def test_get_chat_messages_invalid_id(client):
    chat_id = "1"  
    response = client.get(f"/chats/{chat_id}/messages")

    assert response.status_code == 404
    assert response.json() == {
    "detail": {
    "type": "entity_not_found",
    "entity_name": "Chat",
    "entity_id": "1"
  }
}

 #####################################Delete a chat #############################   
def test_delete_chat_valid_id(client):
    chat_id = "660c7a6bc1324e4488cafabc59529c93"
    response = client.delete(f"/chats/{chat_id}")
    assert response.status_code == 204
    assert response.content== b''

    # test that the delete is persisted
    response = client.get(f"/chats/{chat_id}")
    assert response.status_code == 404
    assert response.json() == {
        "detail": {
            "type": "entity_not_found",
            "entity_name": "Chat",
            "entity_id": chat_id,
        },
    }


def test_delete_chat_invalid_id(client):
    chat_id = "invalid_id"
    response = client.delete(f"/chats/{chat_id}")
    assert response.status_code == 404
    assert response.json() == {
        "detail": {
            "type": "entity_not_found",
            "entity_name": "Chat",
            "entity_id": chat_id,
        },
    }

 #####################################Get Chat User #############################   


def test_get_chat_users_valid_id(client):

    chat_id = "6215e6864e884132baa01f7f972400e2"  
    response = client.get(f"/chats/{chat_id}/users")

    assert response.status_code == 200

    response_data = response.json()
    assert response_data['meta'] == {'count': 2}


def test_get_chat_users_invalid_id(client):
    chat_id = "1"  
    response = client.get(f"/chats/{chat_id}/messages")

    assert response.status_code == 404
    assert response.json() == {
    "detail": {
    "type": "entity_not_found",
    "entity_name": "Chat",
    "entity_id": "1"
  }
}