import pytest
from app import schemas


def test_get_posts(authorized_client, create_posts): 
    res = authorized_client.get('/posts')
    def validate_posts(post):
        return schemas.PostOut(**post)
    
    posts = list(map(validate_posts, res.json()))

    assert len(res.json()) == len(create_posts)
    assert res.status_code == 200 


def test_get_all_posts_unauthorized(client, create_posts): 
    res = client.get('/posts')
    assert res.status_code == 401


def test_get_one_post_unauthorized(client, create_posts): 
    res = client.get('/posts/{create_posts[0].id}')
    assert res.status_code == 401

def test_get_one_post_not_exist(authorized_client, create_posts):
    id = 54
    res = authorized_client.get(f'/posts/{id}')
    assert res.status_code == 404
    assert res.json()['detail'] == f"post with id: {id} does not exist"

def test_get_one_post(authorized_client, create_posts): 
    res = authorized_client.get(f'/posts/{create_posts[0].id}')
    post = schemas.PostOut(**res.json())

    assert res.status_code == 200 
    assert post.Post.id == create_posts[0].id
    assert post.Post.title == create_posts[0].title
    assert post.Post.content == create_posts[0].content

    
@pytest.mark.parametrize("title, content, published", [
    ("post 1", "content 1", True),
    ("post 2", "content 2", False),
    ("post 3", "content 3", True)
])
def test_create_post(authorized_client, user, title, content, published): 
    res = authorized_client.post('/posts', json={'title': title, 'content': content, 'published': published})
    post = schemas.Post(**res.json())
    assert res.status_code == 201 
    assert post.title == title
    assert post.content == content
    assert post.published == published
    assert post.owner_id == user['id']


@pytest.mark.parametrize("title, content", [
    ("post 1", "content 1"),
    ("post 2", "content 2"),
    ("post 3", "content 3")
])
def test_create_post_published_default_true(authorized_client, user, title, content): 
    res = authorized_client.post('/posts', json={'title': title, 'content': content})
    post = schemas.Post(**res.json())
    assert res.status_code == 201 
    assert post.title == title
    assert post.content == content
    assert post.published == True
    assert post.owner_id == user['id']


def test_create_post_unauthorized(client): 
    res = client.post('/posts', json={'title': 'title', 'content': 'content'})
    assert res.status_code == 401


def test_delete_post_unauthorized(client): 
    res = client.delete('/posts/1111')
    res.status_code == 401


def test_delete_post(authorized_client, create_posts): 
    res = authorized_client.delete(f'/posts/{create_posts[0].id}')
    assert res.status_code == 204


def test_delete_post_does_not_exist(authorized_client): 
    res = authorized_client.delete(f'/posts/11')
    assert res.status_code == 404 
    assert res.json()['detail'] == "post with id: 11 does not exist"


def test_delete_post_not_same_owner(authorized_client, create_posts):
    
    post = None
    for pos in create_posts: 
        if pos.title == "post 4":
            post = pos
            break

    
    res = authorized_client.delete(f'/posts/{post.id}')
    res.status_code == 403


@pytest.mark.parametrize("title, content, published", [
    ("post 1", "content 1", True),
    ("post 2", "content 2", False),
    ("post 3", "content 3", True)
])
def test_update_post(authorized_client, create_posts, title, content, published):
    res = authorized_client.put(f'/posts/{create_posts[0].id}', json= {'title':title, 'content':content, 'published': published})
    
    post = schemas.Post(**res.json())
    assert res.status_code == 200 
    assert post.title == title
    assert post.published == published 
    assert post.content == content

def test_update_not_authorized(client, create_posts):
    res = client.put(f'/posts/{create_posts[0].id}')
    assert res.status_code == 401


def test_update_post_not_exist(authorized_client):
    id = 55 
    res = authorized_client.put(f'/posts/{id}', json= {'title': "post 1", 'content':'content', 'published': True})
    res.status_code == 404 
    res.json()['detail'] == f"post with id: {id} does not exist"


def test_update_post_not_same_owner(authorized_client, create_posts):
    post = None
    for pos in create_posts: 
        if pos.title == "post 4":
            post = pos
            break

    res = authorized_client.put(f'/posts/{post.id}', json= {'title': "post 1", 'content':'content', 'published': True})
    res.status_code == 403
    
    