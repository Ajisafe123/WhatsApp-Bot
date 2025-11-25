# core/scheduler.py
import threading
import time
from datetime import datetime
from services.reminder_service import load_reminders, save_reminders, add_reminder
from models.reminder import Reminder
from core.client import wa_client
import pytz

tz = pytz.timezone("Africa/Lagos")

def start_scheduler():
    def run():
        while True:
            now = datetime.now(tz).replace(second=0, microsecond=0)
            reminders = load_reminders()
            for r in reminders[:]:
                next_time = r.remind_time.replace(second=0, microsecond=0)
                if now >= next_time and r.sent_count < r.repeat_count:
                    msg = f"🔔 *REMINDER* #{r.sent_count + 1}\n\n"
                    if r.check_done:
                        msg += f"Have you {r.task.lower()} yet?"
                    else:
                        msg += f"⏰ {r.task}"
                    send_reminder(r)
                    
                    r.sent_count += 1
                    if r.sent_count < r.repeat_count and r.interval_minutes > 0:
                        r.remind_time += timedelta(minutes=r.interval_minutes)
                    save_reminders(reminders)
            time.sleep(60)
    
    threading.Thread(target=run, daemon=True).start()