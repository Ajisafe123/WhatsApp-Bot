# utils/formatter.py
from datetime import datetime

def format_reminder_list(reminders):
    if not reminders:
        return "No active reminders."

    lines = ["*Your Reminders*"]
    for i, r in enumerate(reminders, 1):
        status = "Done" if r.sent_count >= r.repeat_count else "Pending"
        time_str = r.remind_time.strftime("%d %b, %I:%M %p")
        repeat = f" ({r.sent_count}/{r.repeat_count})" if r.repeat_count > 1 else ""
        lines.append(f"{i}. {r.task} → {time_str} [{status}]{repeat}")
    return "\n".join(lines)

def format_reminder_confirmation(reminder):
    lines = [
        "*Reminder Set!*",
        f"*{reminder.task}*",
        f"Date: {reminder.remind_time.strftime('%d %B %Y')}",
        f"Time: {reminder.remind_time.strftime('%I:%M %p')}"
    ]
    if reminder.repeat_count > 1:
        interval = f"every {reminder.interval_minutes} mins" if reminder.interval_minutes else "once"
        lines.append(f"Repeat: {reminder.repeat_count} times ({interval})")
    if reminder.check_done:
        lines.append("Type: Check if done")
    return "\n".join(lines)