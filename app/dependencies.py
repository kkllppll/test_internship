from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.auth import decode_token, get_user_by_username
from app.models.user import User, UserRole
#tells fastapi where to look for the token login endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

#extracts and validates the current user from the JWT token
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    #decode the token and get the username from it
    token_data = decode_token(token)
    if token_data is None:
        raise credentials_exception
    
#check that the user actually exists in the database
    user = get_user_by_username(db, token_data.username)
    if user is None:
        raise credentials_exception
    return user

#accepts multiple roles
def require_role(*roles: UserRole):
    def checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        return current_user
    return checker

#shortcut dependency for admin-only endpoints
def get_admin(current_user: User = Depends(get_current_user)) -> User:
    return require_role(UserRole.admin)(current_user)

#shortcut dependency for editor or admin endpoints
def get_editor_or_admin(current_user: User = Depends(get_current_user)) -> User:
    return require_role(UserRole.editor, UserRole.admin)(current_user)