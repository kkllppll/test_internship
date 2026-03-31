from pydantic import BaseModel

#returned after successful login
class Token(BaseModel):
    access_token: str
    token_type: str  # always "bearer"

#used internally to store data extracted from the token
class TokenData(BaseModel):
    username: str | None = None