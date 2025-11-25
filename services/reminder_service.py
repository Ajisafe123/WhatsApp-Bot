# services/reminder_service.py
import json
from datetime import datetime, timedelta
from models.reminder import Reminder
import pytz

tz = pytz.timezone("Africa/Lagos")
STORAGE_FILE = "storage/reminders.json"

def load_reminders():
    try:
        with open(STORAGE_FILE, "r") as f:
            data = json.load(f)
            return [Reminder.from_dict(r) for r in data]
    except:
        return []

def save_reminders(reminders):
    with open(STORAGE_FILE, "w") as f:
        json.dump([r.to_dict() for r in reminders], f, indent=2)

def add_reminder(reminder):
    reminders = load_reminders()
    # Remove old one if exists
    reminders = [r for r in reminders if r.id != reminder.id]
    reminders.append(reminder)
    save_reminders(reminders)

def get_user_reminders(phone):
    return [r for r in load_reminders() if r.user_phone == phone]

def delete_reminder(reminder_id):
    reminders = load_reminders()
    reminders = [r for r in reminders if r.id != reminder_id]
    save_reminders(reminders)