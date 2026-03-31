


#tests for auth endpoints
def test_login_success(client, admin_user):
    #valid credentials return a token
    response = client.post("/auth/login", data={"username": "admin", "password": "admin123"})
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_wrong_password(client, admin_user):
    #wrong password 401
    response = client.post("/auth/login", data={"username": "admin", "password": "wrongpass"})
    assert response.status_code == 401

def test_login_wrong_username(client, admin_user):
    # non-existent user 401
    response = client.post("/auth/login", data={"username": "nobody", "password": "admin123"})
    assert response.status_code == 401