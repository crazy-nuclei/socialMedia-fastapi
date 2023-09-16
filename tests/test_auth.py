from app import schemas
from app.config import settings
from jose import jwt
import pytest


def test_login(user, client): 
    res = client.post('/login', data={"username": user['email'], "password": user['password']})
    new_token = schemas.Token(**res.json())
    payload = jwt.decode(new_token.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id: int = payload["user_id"]
    assert id == user['id']
    assert new_token.token_type == 'bearer'
    assert res.status_code == 200


@pytest.mark.parametrize("email, password", [
    ("wrong.com","123@123"), ("user@example.com", "wrong")
])
def test_incorrect_login(user, client, email, password): 
    res = client.post('/login', data={"username": email, "password": password})
    assert res.json().get("detail") == "Invalid credentials"
    assert res.status_code == 403