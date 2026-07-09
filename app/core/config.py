from pydantic import BaseSettings, AnyUrl

class Settings(BaseSettings):
    api_football_key: str
    api_football_base: AnyUrl = "https://v3.football.api-sports.io"
    database_url: str = "postgresql://postgres:postgres@postgres:5432/analiz_db"
    redis_url: str = "redis://redis:6379/0"
    secret_key: str = "change-me"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
