from pydantic import BaseModel, EmailStr, Field
from app.models.user import UserRole

#schema for creating a user used in seed script and management commands
class UserCreate(BaseModel):
    username: str = Field(..., example="john_doe", description="Unique username")
    email: EmailStr = Field(..., example="john@example.com", description="User email")
    password: str = Field(..., example="securepassword123", description="Password")
    role: UserRole = Field(default=UserRole.user, description="User role")

#for updating all fields optional for partial updates
class UserUpdate(BaseModel):
    username: str | None = Field(None, example="john_updated", description="New username")
    email: EmailStr | None = Field(None, example="new@example.com", description="New email")

#for returning user data never includes password
class UserResponse(BaseModel):
    id: int = Field(..., example=1)
    username: str = Field(..., example="john_doe")
    email: str = Field(..., example="john@example.com")
    role: UserRole = Field(..., example=UserRole.user)

    # allows converting SQLAlchemy model directly to this schema
    model_config = {"from_attributes": True}