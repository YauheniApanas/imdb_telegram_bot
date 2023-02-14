from pydantic import SecretStr, BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    tg_token: SecretStr = os.getenv("TG_TOKEN", None)
    api_token: SecretStr = os.getenv("API_TOKEN", None)


config = Settings()
