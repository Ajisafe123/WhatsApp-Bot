from fastapi import APIRouter, HTTPException, status
from typing import List
from app.schemas.reminder import ReminderCreate, ReminderResponse
from app.services.reminder_service import ReminderService

router = APIRouter()
reminder_service = ReminderService()


@router.post("/create", response_model=ReminderResponse, status_code=status.HTTP_201_CREATED)
async def create_reminder(reminder: ReminderCreate):
    try:
        new_reminder = await reminder_service.create_reminder(reminder)
        return new_reminder
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=List[ReminderResponse])
async def list_reminders(phone_number: str = None):
    try:
        reminders = await reminder_service.list_reminders(phone_number)
        return reminders
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{reminder_id}", response_model=ReminderResponse)
async def get_reminder(reminder_id: str):
    try:
        reminder = await reminder_service.get_reminder(reminder_id)
        if not reminder:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reminder not found")
        return reminder
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{reminder_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_reminder(reminder_id: str):
    try:
        await reminder_service.delete_reminder(reminder_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
