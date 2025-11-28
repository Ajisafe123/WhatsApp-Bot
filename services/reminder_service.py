import json
import os
from models.reminder import Reminder
from utils.logger import logger
from datetime import datetime
import pytz

tz = pytz.timezone("Africa/Lagos")
STORAGE_FILE = os.getenv("REMINDER_STORAGE", "storage/reminders.json")

os.makedirs(os.path.dirname(STORAGE_FILE), exist_ok=True)

def load_reminders():
    try:
        with open(STORAGE_FILE, "r") as f:
            data = json.load(f)
            return [Reminder.from_dict(r) for r in data]
    except FileNotFoundError:
        return []
    except Exception:
        logger.exception("Failed to load reminders")
        return []

def save_reminders(reminders):
    try:
        with open(STORAGE_FILE, "w") as f:
            json.dump([r.to_dict() for r in reminders], f, indent=2)
    except Exception:
        logger.exception("Failed to save reminders")

def add_reminder(reminder):
    reminders = load_reminders()
    reminders = [r for r in reminders if r.id != reminder.id]
    reminders.append(reminder)
    save_reminders(reminders)

def list_reminders(phone):
    return [r for r in load_reminders() if r.user_phone == phone]

def delete_reminder(phone, index):
    reminders = load_reminders()
    user_reminders = [r for r in reminders if r.user_phone == phone]
    if 0 <= index < len(user_reminders):
        reminders.remove(user_reminders[index])
        save_reminders(reminders)

async def check_pending_reminders():
    return
