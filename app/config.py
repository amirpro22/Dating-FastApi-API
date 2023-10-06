

from pydantic import BaseSettings,root_validator

class Settings(BaseSettings):
    DB_HOST : str
    DB_PORT : int
    DB_USER : str
    DB_PASS : str
    DB_NAME : str
    ACCESS_SECRET_KEY : str
    REFRESH_SECRET_KEY : str
    ALGORITHM : str
    AWS_ACCESS_KEY_ID : str
    AWS_SECRET_ACCESS_KEY : str
    AWS_BUCKET : str
    AWS_REGION : str
    REDIS_HOST : str
    REDIS_PORT : int
    REDIS_PASSWORD : str
    REDIS_DATABASE : str
    
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def REDIS_URL(self) -> str:
        return f"redis://arbitrary_usrname:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DATABASE}"


    class Config:
        env_file = ".env"

settings = Settings()


