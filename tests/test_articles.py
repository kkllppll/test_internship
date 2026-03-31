


# tests for article endpoints
from app.models.article import Article

def test_create_article(client, user_token):
    #authenticated user should be able to create an article
    response = client.post(
        "/articles/",
        json={"title": "Test", "content": "Test content"},
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 201
    assert response.json()["title"] == "Test"

def test_get_articles(client, user_token):
    #authenticated user should be able to get all articles
    response = client.get("/articles/", headers={"Authorization": f"Bearer {user_token}"})
    assert response.status_code == 200

def test_get_articles_unauthorized(client):
    #request without token  401
    response = client.get("/articles/")
    assert response.status_code == 401

def test_delete_own_article(client, user_token, regular_user, db):
    #user should be able to delete their own article
    article = Article(title="Mine", content="My content", author_id=regular_user.id)
    db.add(article)
    db.commit()
    db.refresh(article)

    response = client.delete(
        f"/articles/{article.id}",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 204

def test_delete_others_article_as_user(client, user_token, admin_user, db):
    #user should not be able to delete someone elses article
    article = Article(title="Admin article", content="Content", author_id=admin_user.id)
    db.add(article)
    db.commit()
    db.refresh(article)

    response = client.delete(
        f"/articles/{article.id}",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 403