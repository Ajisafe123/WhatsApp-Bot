from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class ReminderCreate(BaseModel):
    user_phone: str = Field(..., description="User's WhatsApp phone number")
    reminder_text: str = Field(..., description="Text of the reminder")
    scheduled_time: datetime = Field(..., description="When to send the reminder")


class ReminderUpdate(BaseModel):
    reminder_text: Optional[str] = None
    scheduled_time: Optional[datetime] = None
    status: Optional[str] = None


class ReminderResponse(BaseModel):
    id: str = Field(..., alias="_id")
    user_phone: str
    reminder_text: str
    scheduled_time: datetime
    status: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        populate_by_name = True
