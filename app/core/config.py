from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    TWILIO_ACCOUNT_SID: str
    TWILIO_AUTH_TOKEN: str
    TWILIO_PHONE_NUMBER: str
    
    MONGODB_URL: str
    MONGODB_DB_NAME: str = "whatsapp_bot"
    
    API_TITLE: str = "WhatsApp Reminder Bot"
    API_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
