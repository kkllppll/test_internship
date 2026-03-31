from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.config import settings

#create_engine connects to the database using the url from .env
engine = create_engine(settings.DATABASE_URL)

#SessionLocal is a factory for database sessions
#autocommit=False we control when to save changes
#autoflush=False changes not sent to db until we commit
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#base class for all sqllchemy models
class Base(DeclarativeBase):
    pass

#yield gives the session finally closes it after the request is done
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()