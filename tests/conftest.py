import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from app.models.user import User, UserRole
from app.services.auth import hash_password

#sqlite for tests
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#runs before and after every test fresh tables each time
@pytest.fixture(scope="function", autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

#provides a test database session
@pytest.fixture
def db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

#provides a test client that uses the test db instead of real postgres
@pytest.fixture
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass
    #replace the real db dependency with the test one
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

#creates an admin user in the test db
@pytest.fixture
def admin_user(db):
    user = User(
        username="admin",
        email="admin@test.com",
        hashed_password=hash_password("admin123"),
        role=UserRole.admin
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

#creates a regular user in the test db
@pytest.fixture
def regular_user(db):
    user = User(
        username="user1",
        email="user1@test.com",
        hashed_password=hash_password("user123"),
        role=UserRole.user
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

#logs in as admin and returns the jwt 
@pytest.fixture
def admin_token(client, admin_user):
    response = client.post("/auth/login", data={"username": "admin", "password": "admin123"})
    return response.json()["access_token"]

#logs in as regular user and returns the jwt 
@pytest.fixture
def user_token(client, regular_user):
    response = client.post("/auth/login", data={"username": "user1", "password": "user123"})
    return response.json()["access_token"]