from pydantic import BaseModel, Field
from datetime import datetime

#schema for creating a new article only title and content required
class ArticleCreate(BaseModel):
    title: str = Field(..., example="My First Article", description="Title")
    content: str = Field(..., example="This is the content of my article.", description="Content")
#for updating all fields optional so partial updates work
class ArticleUpdate(BaseModel):
    title: str | None = Field(None, example="Updated Title", description="New title")
    content: str | None = Field(None, example="Updated content.", description="New content")

#for returning article data in responses never includes sensitive data
class ArticleResponse(BaseModel):
    id: int = Field(..., example=1)
    title: str = Field(..., example="My First Article")
    content: str = Field(..., example="This is the content of my article.")
    author_id: int = Field(..., example=1)
    created_at: datetime
    updated_at: datetime | None = None

    #allows converting sqlalchemy model directly to this schema
    model_config = {"from_attributes": True}