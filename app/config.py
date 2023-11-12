from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str = "localhost"
    DB_DATABASE: str = "postgres"
    OAUTH_SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60


config = Settings()
