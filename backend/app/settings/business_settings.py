from pydantic_settings import BaseSettings, SettingsConfigDict
class _BusinessSettings(BaseSettings):
    ADMIN_ROLE: str
    DEFAULT_USER_ROLE_ID: int
    DEFAULT_ADMIN_ROLE_ID: int
    ADMIN_PASSWORD: str

    model_config = SettingsConfigDict(env_file="settings/.env.business")

business_settings = _BusinessSettings()