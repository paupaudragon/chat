from datetime import datetime

from fastapi.testclient import TestClient

from backend.main import app

#################### Get all users ####################
def test_get_all_users():
    client = TestClient(app)
    response = client.get("/users")
    assert response.status_code == 200

    meta = response.json()["meta"]
    users = response.json()["users"]
    assert meta["count"] == len(users)
    assert users == sorted(users, key=lambda user: user["id"])

def test_get_all_users_sorted_by_createdAt():
    client = TestClient(app)
    response = client.get("/users?sort=created_at")
    assert response.status_code == 422
    assert response.json()['detail'][0]['type'] == "literal_error"
    

def test_get_all_users_sorted_by_non_exsit_attr():
    client = TestClient(app)
    response = client.get("/users?sort=name")
    assert response.status_code == 422
    assert response.json()['detail'][0]['type'] == "literal_error"


#################### Create a User ####################
def test_create_valid_user():
    create_params = {"id": "tzhou"}
    client = TestClient(app)
    response = client.post("/users", json=create_params)

    assert response.status_code == 200
    user = response.json()
    for key, value in create_params.items():
        assert user['user'][key]==value

    response = client.get(f"/users/{user['user']['id']}")
    assert response.status_code == 200
    user = response.json()
    for key, value in create_params.items():
        assert user['user'][key] == value

def test_create_existing_user():
    create_params = {"id": "newt"}
    client = TestClient(app)
    response = client.post("/users", json=create_params)

    assert response.status_code == 422
    assert response.json() == {
        "detail": {
                "type": "duplicate_entity",
                "entity_name": "User",
                "entity_id": create_params["id"],
            },
    }

#################### Get a User by id ####################
def test_get_user_valid_id():
    user_id = "burke"
    expected_response = {'user': {'created_at': '2018-07-25T10:40:45', 'id': 'burke'}}
    client = TestClient(app)
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json() == expected_response

def test_get_user_invalid_id():
    user_id = "z"
    client = TestClient(app)
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 404
    
    assert response.json() == {
        "detail": {
            "type": "entity_not_found",
            "entity_name": "User",
            "entity_id": user_id,
        },
    }
#################### Get chats of a user ####################
def test_get_user_chats_valid_id():

    user_id = "ripley"  
    client = TestClient(app)
    response = client.get(f"/users/{user_id}/chats")

    assert response.status_code == 200
    expected = {
  "meta": {
    "count": 2
  },
  "chats": [
    {
      "id": "e0ec0881a2c645de842ca5dd0fa7985b",
      "name": "newt",
      "user_ids": [
        "newt",
        "ripley"
      ],
      "owner_id": "ripley",
      "created_at": "2023-12-13T17:26:45"
    },
    {
      "id": "734eeb9ddaec43b2ab6e289a0d472376",
      "name": "nostromo",
      "user_ids": [
        "bishop",
        "burke",
        "ripley"
      ],
      "owner_id": "ripley",
      "created_at": "2023-09-18T14:18:46"
    }
  ]
}
    response_data = response.json()
    assert response_data == expected


def test_get_user_chats_invalid_id():
    user_id = "1"  
    client = TestClient(app)
    response = client.get(f"/users/{ user_id}/chats")

    assert response.status_code == 404
    assert response.json() == {
    "detail": {
    "type": "entity_not_found",
    "entity_name": "User",
    "entity_id": "1"
  }
}
        
        
