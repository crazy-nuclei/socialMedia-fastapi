

def test_votes_unauthorized(client, create_posts): 
    data = {
        'post_id': create_posts[0].id,
        'dir': 1
    }
    res = client.post('/votes', json= data)
    assert res.status_code == 401


def test_votes_add_vote_not_present(authorized_client, create_posts): 
    data = {
        'post_id': create_posts[1].id,
        'dir': 1
    }
    res = authorized_client.post('/votes', json= data)
    assert res.status_code == 201 
    assert res.json()['status'] ==  "successfully added vote"


def test_votes_add_vote_present(authorized_client, user, create_posts, create_votes):
    data = {
        'post_id': create_posts[0].id,
        'dir': 1
    }
    res = authorized_client.post('/votes', json= data)
    assert res.status_code == 409
    assert res.json()['detail'] == f"user: {user['id']} has already voted on post: {data['post_id']}"


def test_votes_delete_vote_present(authorized_client, user, create_posts, create_votes):
    data = {
        'post_id': create_posts[0].id,
        'dir': 0
    }
    res = authorized_client.post('/votes', json= data)
    assert res.status_code == 201
    assert res.json()["status"] == "successfully deleted vote"


def test_votes_delete_vote_not_present(authorized_client, user, create_posts):
    data = {
        'post_id': create_posts[1].id,
        'dir': 0
    }
    res = authorized_client.post('/votes', json= data)
    assert res.status_code == 409
    assert res.json()['detail'] == f"user: {user['id']} has not voted on post: {data['post_id']}"


def test_vote_post_not_exist(authorized_client):
    data = {
        'post_id': 1,
        'dir': 1
    }
    res = authorized_client.post('/votes', json=data)
    assert res.status_code == 404
    assert res.json()['detail'] == f"Post with id: {data['post_id']} doesn't exist "