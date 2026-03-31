

#tests for user endpoints
def test_get_me(client, user_token):
    #authenticated user get their own data
    response = client.get("/users/me", headers={"Authorization": f"Bearer {user_token}"})
    assert response.status_code == 200
    assert response.json()["username"] == "user1"

def test_get_me_unauthorized(client):
    #request without token 401
    response = client.get("/users/me")
    assert response.status_code == 401

def test_get_users_as_admin(client, admin_token):
    #admin should be able to list all users
    response = client.get("/users/", headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200

def test_get_users_as_user(client, user_token):
    #regular user should not be able to list all users
    response = client.get("/users/", headers={"Authorization": f"Bearer {user_token}"})
    assert response.status_code == 403

def test_delete_user_as_admin(client, admin_token, regular_user):
    #admin should be able to delete any user
    response = client.delete(f"/users/{regular_user.id}", headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 204