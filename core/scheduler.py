import threading
import time
from datetime import datetime, timedelta
from services.reminder_service import load_reminders, save_reminders
from core.client import wa_client
import pytz

tz = pytz.timezone("Africa/Lagos")

def send_reminder(reminder):
    msg = f"🔔 *REMINDER* #{reminder.sent_count + 1}\n\n"
    msg += f"⏰ {reminder.task}"
    wa_client.send_message(reminder.user_phone, msg)

def start_scheduler():
    def run():
        while True:
            now = datetime.now(tz).replace(microsecond=0)
            reminders = load_reminders()
            updated = False
            for r in reminders[:]:
                next_time = r.remind_time.replace(microsecond=0)
                if now >= next_time and r.sent_count < r.repeat_count:
                    send_reminder(r)
                    r.sent_count += 1
                    if r.sent_count < r.repeat_count:
                        r.remind_time += timedelta(minutes=r.interval_minutes, seconds=r.interval_seconds)
                    updated = True
            if updated:
                save_reminders(reminders)
            time.sleep(1)
    threading.Thread(target=run, daemon=True).start()
