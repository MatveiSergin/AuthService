from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
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
    @property
    def DATABASE_URL(self):
        return f"{self.DB_DIALECT}+{self.DB_DRIVER}://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DATABASE}"


    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()