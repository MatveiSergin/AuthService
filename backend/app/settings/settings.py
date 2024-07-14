from pydantic_settings import BaseSettings, SettingsConfigDict
from sys import platform
class _Settings(BaseSettings):
    DB_DIALECT: str
    DB_DRIVER: str
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DATABASE: str
    AUTH_SECRET: str
    AUTH_RESET_SECRET: str
    ENGINE_ECHO: bool = True
    ENGINE_POOL_SIZE: int = 10
    EXPIRE_REDIS: int
    PATH_TO_REQUEST_LOG: str
    PATH_TO_DATABASE_LOG: str
    @property
    def DATABASE_URL(self):
        return f"{self.DB_DIALECT}+{self.DB_DRIVER}://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DATABASE}"

    @staticmethod
    def env_file():
        if platform == "win32":
            return "settings/.env"
        else:
            return "settings/.env.ubuntu"

    model_config = SettingsConfigDict(env_file=env_file())

settings = _Settings()