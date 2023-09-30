from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    app_name: str = "Github users scraper"
    db_url:str="postgresql://postgres:secretpass@postgres:5432/gitusers"

    model_config = SettingsConfigDict(env_file=".env",extra="allow")

@lru_cache()
def get_settings():
    return Settings()

""" print("config.py called") """