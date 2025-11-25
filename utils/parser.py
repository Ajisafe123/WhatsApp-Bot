# utils/parser.py
from datetime import datetime
import re
import pytz

tz = pytz.timezone("Africa/Lagos")

def parse_reminder(text, phone):
    text = text.lower()
    now = datetime.now(tz)

    # Extract time
    time_match = re.search(r"(\d{1,2}:\d{2}\s*(?:am|pm))|(\d{1,2}\s*(?:am|pm))", text)
    if not time_match:
        return None
    time_str = time_match.group(0)

    # Parse time
    try:
        remind_time = datetime.strptime(time_str, "%I:%M %p" if ":" in time_str else "%I %p")
        remind_time = remind_time.replace(year=now.year, month=now.month, day=now.day)
        if remind_time < now:
            remind_time += timedelta(days=1)
        remind_time = tz.localize(remind_time)
    except:
        return None

    # Task
    task = text.split("remind me")[1].split("by")[0].split("if i have")[0].strip()

    # Check "if I have done"
    check_done = "if i have" in text or "if i've" in text

    # Repeat?
    repeat_match = re.search(r"(\d+) ?x", text)
    repeat_count = int(repeat_match.group(1)) if repeat_match else 1

    # Interval?
    interval_match = re.search(r"every (\d+) ? ?(mins|minutes|hours?)", text)
    interval = 0
    if interval_match:
        num = int(interval_match.group(1))
        unit = interval_match.group(2)
        interval = num * 60 if "hour" in unit else num

    from models.reminder import Reminder
    return Reminder(phone, task, remind_time, repeat_count, interval, check_done)