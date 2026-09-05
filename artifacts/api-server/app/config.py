import os

from dotenv import load_dotenv


load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///pragatisahayak.db",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET = os.environ.get("JWT_SECRET", "default_secret_key")
    LLM_API_KEY = os.environ.get("LLM_API_KEY", "")
    FLASK_ENV = os.environ.get("FLASK_ENV", "development")