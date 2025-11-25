# models/reminder.py
from datetime import datetime
import pytz

tz = pytz.timezone("Africa/Lagos")

class Reminder:
    def __init__(self, user_phone, task, remind_time, repeat_count=1, interval_minutes=0, check_done=False):
        self.user_phone = user_phone
        self.task = task.strip().capitalize()
        self.remind_time = remind_time  # datetime object
        self.repeat_count = repeat_count
        self.interval_minutes = interval_minutes
        self.check_done = check_done  # "if I have done" style
        self.sent_count = 0
        self.id = f"{user_phone}_{int(remind_time.timestamp())}"

    def to_dict(self):
        return {
            "user_phone": self.user_phone,
            "task": self.task,
            "remind_time": self.remind_time.isoformat(),
            "repeat_count": self.repeat_count,
            "interval_minutes": self.interval_minutes,
            "check_done": self.check_done,
            "sent_count": self.sent_count,
            "id": self.id
        }

    @staticmethod
    def from_dict(data):
        r = Reminder(
            user_phone=data["user_phone"],
            task=data["task"],
            remind_time=datetime.fromisoformat(data["remind_time"]),
            repeat_count=data["repeat_count"],
            interval_minutes=data["interval_minutes"],
            check_done=data["check_done"]
        )
        r.sent_count = data.get("sent_count", 0)
        r.id = data["id"]
        return r