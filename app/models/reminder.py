from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from bson import ObjectId


class ReminderModel(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    user_phone: str
    reminder_text: str
    scheduled_time: datetime
    status: str = "pending"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "user_phone": "whatsapp:+1234567890",
                "reminder_text": "Don't forget your meeting!",
                "scheduled_time": "2024-01-01T10:00:00",
                "status": "pending"
            }
        }
