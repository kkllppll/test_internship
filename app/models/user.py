from sqlalchemy import Column, Integer, String, Enum
from app.database import Base
import enum

#limits possible values to these three
class UserRole(str, enum.Enum):
    user = "user"       #can manage own articles only
    editor = "editor"   #can view and update any article
    admin = "admin"     #full access to everything

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)

    #password is never stored in plain text only the hashed version
    hashed_password = Column(String, nullable=False)
    
    #role is assigned on creation defaults to regular user
    role = Column(Enum(UserRole), default=UserRole.user, nullable=False)