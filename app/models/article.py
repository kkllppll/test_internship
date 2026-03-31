from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False, index=True)
    content = Column(Text, nullable=False)
 
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    #onupdate automatically sets the timestamp whenever the article is edited
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    #relationship allowsto access article.author directly
    author = relationship("User", backref="articles")