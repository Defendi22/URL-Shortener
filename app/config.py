from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "postgresql://postgres:postgres@localhost:5432/urlshortener"
    secret_key: str = "dev-secret-change-in-production"
    base_url: str = "http://localhost:8000"
    code_length: int = 6

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()