from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

users = [
    {
        'id': 1,
        'name': 'Ivan Ivanov',
        'email': 'i.i.ivanov@mail.com',
    },
    {
        'id': 2,
        'name': 'Petr Petrov',
        'email': 'p.p.petrov@mail.com',
    }
]

def test_get_existed_user():
    response = client.get("/api/v1/user", params={'email': users[0]['email']})
    assert response.status_code == 200
    assert response.json() == users[0]

def test_get_unexisted_user():
    response = client.get("/api/v1/user", params={'email': 'unknown@mail.com'})
    assert response.status_code == 404
    assert response.json() == {'detail': 'User not found'}

def test_create_user_with_valid_email():
    new_user = {
        'id': 3,
        'name': 'Sidor Sidorov',
        'email': 's.sidorov@mail.com'
    }
    response = client.post("/api/v1/user", json=new_user)
    assert response.status_code == 201
    assert response.json() == new_user

def test_create_user_with_invalid_email():
    duplicate_user = {
        'id': 4,
        'name': 'Duplicate',
        'email': users[0]['email']
    }
    response = client.post("/api/v1/user", json=duplicate_user)
    assert response.status_code == 409
    assert response.json() == {'detail': 'User already exists'}

def test_delete_user():
    user_email = users[1]['email']
    response = client.delete("/api/v1/user", params={'email': user_email})
    assert response.status_code == 204
    assert response.json() == {'message': f'User {user_email} deleted'}
    
    get_response = client.get("/api/v1/user", params={'email': user_email})
    assert get_response.status_code == 404
