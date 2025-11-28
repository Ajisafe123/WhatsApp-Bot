import threading
import time
from datetime import datetime, timedelta
from services.reminder_service import load_reminders, save_reminders
from core.client import wa_client
import pytz
from utils.logger import logger

tz = pytz.timezone("Africa/Lagos")

def send_reminder_message(reminder):
    msg = f"🔔 *REMINDER* #{reminder.sent_count + 1}\n\n"
    msg += f"⏰ {reminder.task}"
    wa_client.send_message(reminder.user_phone, msg)
    logger.info(f"Sent reminder to {reminder.user_phone}: {reminder.task}")

def start_scheduler():
    def run():
        logger.info("Scheduler started (checks every 1s)")
        while True:
            now = datetime.now(tz).replace(microsecond=0)
            reminders = load_reminders()
            updated = False
            for r in reminders[:]:
                next_time = r.remind_time.replace(microsecond=0)
                if now >= next_time and r.sent_count < r.repeat_count:
                    try:
                        send_reminder_message(r)
                        r.sent_count += 1
                        if r.sent_count < r.repeat_count:
                            interval = getattr(r, "interval_seconds", 0) or r.interval_minutes * 60
                            r.remind_time = r.remind_time + timedelta(seconds=interval)
                        updated = True
                    except Exception:
                        logger.exception("Error sending reminder")
            if updated:
                save_reminders(reminders)
            time.sleep(1)

    threading.Thread(target=run, daemon=True).start()