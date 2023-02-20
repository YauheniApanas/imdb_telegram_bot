from pydantic import SecretStr, BaseSettings
import os


class Settings(BaseSettings):
    tg_token: SecretStr = os.getenv("TG_TOKEN", None)
    api_token: SecretStr = os.getenv("API_TOKEN", None)


config = Settings()
