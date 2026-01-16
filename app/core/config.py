from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    kinorium_base_url: str = "https://ua.kinorium.com"
    default_timeout: int = 15000
    default_wait_time: int = 10000
    user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    port: int = 8080
    cache_expire: int = 3600

settings = Settings()
