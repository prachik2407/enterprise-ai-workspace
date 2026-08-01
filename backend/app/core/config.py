from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str
    ENVIRONMENT: str

    model_config = SettingsConfigDict(
    env_file=".env",
    extra="ignore"
)

settings = Settings()