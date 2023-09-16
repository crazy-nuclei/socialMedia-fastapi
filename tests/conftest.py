from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings
from app.database import Base, get_db
from app.main import app
from fastapi.testclient import TestClient
import pytest
from app import schemas, models 
from app.oauth2 import create_access_token

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

# postgresql://<username>:<password>@<ip-address/hostname>:<post_no>/<database_name>

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


@pytest.fixture
def session(): 
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session): 
    # Dependency
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


@pytest.fixture
def user(client): 
    res = client.post("/users", json={"email": "user@example.com", "password": "123"})
    user = schemas.UserOut(**res.json())
    user = user.model_dump()
    user['password'] = '123'
    return user


@pytest.fixture
def user2(client): 
    res = client.post("/users", json={"email": "user2@example.com", "password": "123"})
    user = schemas.UserOut(**res.json())
    user = user.model_dump()
    user['password'] = '123'
    return user


@pytest.fixture
def token(user): 
    token = create_access_token({"user_id": user['id']})
    return token


@pytest.fixture 
def authorized_client(client, token): 
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}
    return client


@pytest.fixture
def create_posts(session, user, user2): 
    data = [
        {'title': 'post 1', 'content': 'content 1', 'owner_id': user['id']},
        {'title': 'post 2', 'content': 'content 2', 'owner_id': user['id']},
        {'title': 'post 3', 'content': 'content 3', 'owner_id': user['id']},
        {'title': 'post 4', 'content': 'content 4', 'owner_id': user2['id']}
    ]

    def create_post_model(post): 
        return models.Post(**post)
    
    posts = list(map(create_post_model, data))

    session.add_all(posts)
    session.commit()

    posts = session.query(models.Post).all()
    return posts


@pytest.fixture
def create_votes(session, create_posts, user): 
    data = [
        {'post_id': create_posts[0].id, 'user_id': user['id']},
    ]

    def create_vote_model(vote): 
        return models.Vote(**vote)
    
    votes = list(map(create_vote_model, data))

    session.add_all(votes)
    session.commit()



