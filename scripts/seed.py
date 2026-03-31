import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, Base, engine
from app.models.user import User, UserRole
from app.models.article import Article
from app.services.auth import hash_password

#creating tables if they don't exist yet
Base.metadata.create_all(bind=engine)

def seed():
    db = SessionLocal()
    try:
        #skiing seeding if data already exists
        if db.query(User).first():
            print("Database already seeded!")
            return

        #create one user for each role
        users = [
            User(username="admin", email="admin@test.com",
                 hashed_password=hash_password("admin123"), role=UserRole.admin),
            User(username="editor", email="editor@test.com",
                 hashed_password=hash_password("editor123"), role=UserRole.editor),
            User(username="user1", email="user1@test.com",
                 hashed_password=hash_password("user123"), role=UserRole.user),
        ]
        db.add_all(users)
        db.commit()

        #refresh to get the auto generated id s
        for u in users:
            db.refresh(u)

        #create sample articles with different authors
        articles = [
            Article(title="First Article", content="Content of first article", author_id=users[2].id),
            Article(title="Second Article", content="Content number two article", author_id=users[1].id),
            Article(title="Another Article", content="More content here", author_id=users[2].id),
        ]
        db.add_all(articles)
        db.commit()

        print("Database seeded successfully!")
        print("admin / admin123")
        print("editor / editor123")
        print("user1 / user123")

    finally:
        #close session even if fail
        db.close()


if __name__ == "__main__":
    seed()