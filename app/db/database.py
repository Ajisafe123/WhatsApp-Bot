from motor.motor_asyncio import AsyncClient, AsyncDatabase
from app.core.config import settings
from typing import Optional


class Database:
    client: Optional[AsyncClient] = None
    db: Optional[AsyncDatabase] = None
    
    @classmethod
    async def connect_db(cls):
        cls.client = AsyncClient(settings.MONGODB_URL)
        cls.db = cls.client[settings.MONGODB_DB_NAME]
        print("Connected to MongoDB")
    
    @classmethod
    async def close_db(cls):
        if cls.client:
            cls.client.close()
            print("Disconnected from MongoDB")
    
    @classmethod
    def get_db(cls) -> AsyncDatabase:
        return cls.db


async def get_db() -> AsyncDatabase:
    return Database.get_db()
