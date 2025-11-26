from datetime import datetime, timedelta
import pytz
from dateutil import parser as date_parser
import re
from models.reminder import Reminder

tz = pytz.timezone("Africa/Lagos")

def parse_reminder_command(text, phone):
    """
    Parses commands like:
      'remind me to [task] by [time] xN every [interval]'
      'remind me to [task] in 10s x5 every 3s'
    Supports:
      - Absolute times: 3pm, 15:30
      - Relative times: in 5s, 2min, 3h
      - Repeat: x5
      - Interval: every 1s/m/h
      - Multiple tasks using 'and'
    """
    text = text.lower().strip()
    now = datetime.now(tz)

    reminders = []
    parts = re.split(r"\band\b", text)

    for part in parts:
        part = part.strip()
        repeat_match = re.search(r"x(\d+)", part)
        repeat_count = int(repeat_match.group(1)) if repeat_match else 1
        interval_match = re.search(r"every (\d+)\s*(s|sec|second|seconds|m|min|minute|minutes|h|hr|hour|hours)", part)
        interval_minutes = 0
        interval_seconds = 0
        if interval_match:
            num = int(interval_match.group(1))
            unit = interval_match.group(2)
            if unit.startswith("h"):
                interval_minutes = num * 60
            elif unit.startswith("m"):
                interval_minutes = num
            else:
                interval_seconds = num
        time_match = re.search(r"\bby (.+)|\bin (.+)", part)
        if not time_match:
            continue
        time_str = time_match.group(1) or time_match.group(2)
        time_str = time_str.strip()

        remind_time = None
        rel_match = re.match(r"(?:(\d+)\s*(s|sec|second|seconds|m|min|minute|minutes|h|hr|hour|hours))", time_str)
        if rel_match:
            num = int(rel_match.group(1))
            unit = rel_match.group(2)
            if unit.startswith("h"):
                remind_time = now + timedelta(hours=num)
            elif unit.startswith("m"):
                remind_time = now + timedelta(minutes=num)
            else:
                remind_time = now + timedelta(seconds=num)
        else:
            try:
                remind_time = date_parser.parse(time_str, default=now)
            except:
                continue

        if remind_time.tzinfo is None:
            remind_time = tz.localize(remind_time)
        if remind_time < now:
            remind_time += timedelta(days=1)

        # Task
        task_match = re.search(r"remind me to (.+?) (?:by|in)", part)
        if not task_match:
            continue
        task = task_match.group(1).strip()

        reminder = Reminder(phone, task, remind_time, repeat_count=repeat_count, interval_minutes=interval_minutes, interval_seconds=interval_seconds)

        reminders.append({
            "id": reminder.id,
            "user_phone": phone,
            "task": reminder.task,
            "time": remind_time.strftime("%I:%M:%S %p"),
            "remind_time": remind_time,
            "repeat_count": repeat_count,
            "interval_minutes": interval_minutes,
            "interval_seconds": interval_seconds
        })

    return reminders if reminders else None
