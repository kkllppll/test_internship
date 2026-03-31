from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.auth import authenticate_user, create_access_token
from app.schemas.token import Token

router = APIRouter(prefix="/auth", tags=["auth"])
@router.post(
    "/login",
    response_model=Token,
    summary="Get JWT token",
    description="Login with username and password. Returns a JWT token for authorization."
)
def login(
    #reads username and password from form data
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    #store username in the token payload under sub
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}