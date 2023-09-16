from app import schemas

def test_root(client):
    response = client.get("/")
    assert response.json().get("message") == "Welcome to my API !!!"
    assert response.status_code == 200 

def test_create_user(client):
    response = client.post("/users", json={"email": "user@example.com", "password": "password@123"})
    new_user = schemas.UserOut(**response.json())
    assert new_user.email == "user@example.com"
    assert response.status_code == 201
