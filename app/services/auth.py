from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.token import TokenData
from app.config import settings
from datetime import datetime, timezone

datetime.now(timezone.utc)

#for hashing and verifying passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#returns a bcrypt hash of the given password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

#compares a plain password against a stored hash true/false
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

#creates a signed jwt token with an expiration time
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
    minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

#fetches a user from the database by username
def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

#verifies username and password returns the user or none if invalid
def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

#decodes a jwt token and returns the username stored inside
#returns none if the token is invalid or expired
def decode_token(token: str) -> TokenData | None:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
        return TokenData(username=username)
    except JWTError:
        return None