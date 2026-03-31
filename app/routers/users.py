from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User, UserRole
from app.schemas.user import UserResponse, UserUpdate
from app.dependencies import get_current_user, require_role
from typing import List

router = APIRouter(prefix="/users", tags=["users"])


@router.get(
    "/",
    response_model=List[UserResponse],
    summary="Get all users",
    description="Returns a list of all users. Admin only. Supports search by username, limit and offset."
)
def get_users(
    search: str | None = None,
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db),
    #only admin can see all users
    current_user: User = Depends(require_role(UserRole.admin))
):
    query = db.query(User)
    #case insensitive search by username
    if search:
        query = query.filter(User.username.ilike(f"%{search}%"))
    return query.offset(offset).limit(limit).all()

@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user",
    description="Returns information about the currently authenticated user."
)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Get user by ID",
    description="Returns a user by ID. Available to any authenticated user."
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Update user",
    description="Updates user data. A user can update only themselves. Admin can update anyone."
)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    #check permissions before querying the db
    if current_user.id != user_id and current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    #only update fields that were actually provided 
    for field, value in user_data.model_dump(exclude_none=True).items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user

@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete user",
    description="Deletes a user by ID. Admin only."
)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.admin))
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()