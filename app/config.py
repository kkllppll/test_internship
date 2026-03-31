from pydantic_settings import BaseSettings

#settings class automatically reads values from .env
class Settings(BaseSettings):
    #required fields app won't start if these are missing in .env
    DATABASE_URL: str
    SECRET_KEY: str

    #optional fields with default values
    ALGORITHM: str = "HS256"  #algorithm used for JWT encoding
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  #how long the token is valid

    #postgres credentials used by docker\
    POSTGRES_USER: str = ""
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = ""

    model_config = {"env_file": ".env", "extra": "ignore"}
settings = Settings()