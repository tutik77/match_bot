from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    openai_api_key: str
    bot_token: str
    db_host: str
    db_name: str
    db_collection: str

    class Config:
        env_file= ".env"

settings = Settings()