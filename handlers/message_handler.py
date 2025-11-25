# handlers/message_handler.py
from pywa.types import Message, Button
from pywa.types.callback import Section, SectionList
from utils.parser import parse_reminder
from services.reminder_service import add_reminder, get_user_reminders, delete_reminder
from core.scheduler import start_scheduler
from config.settings import ALLOWED_USERS
from utils.formatter import format_reminder_list
from utils.logger import logger

# Start scheduler once
start_scheduler()

def handle_message(client: "WhatsApp", msg: Message):
    if msg.from_user.phone not in ALLOWED_USERS:
        msg.reply("❌ Unauthorized")
        return

    text = msg.text.strip().lower() if msg.text else ""

    if text in ["hi", "hello", "menu", "start"]:
        msg.reply(
            text="🔔 *Smart Reminder Bot*\n\n"
                 "Examples:\n"
                 "• remind me to wash clothes by 3pm\n"
                 "• remind me if i have eaten by 8am\n"
                 "• remind me 5x to drink water every 30 mins\n"
                 "• my reminders / cancel 2",
            buttons=[
                Button(title="Set Reminder", callback_data="set"),
                Button(title="My Reminders", callback_data="list")
            ]
        )

    elif "remind me" in text:
        reminder = parse_reminder(msg.text, msg.from_user.phone)
        if reminder:
            add_reminder(reminder)
            msg.react("✅")
            repeat_text = f"{reminder.repeat_count}x every {reminder.interval_minutes} mins" if reminder.repeat_count > 1 else ""
            msg.reply(f"⏰ Reminder Set!\n\n"
                      f"*{reminder.task}*\n"
                      f"📅 {reminder.remind_time.strftime('%d %b, %I:%M %p')}\n"
                      f"🔁 {repeat_text}")
        else:
            msg.reply("❌ Invalid format. Try:\nremind me to call mom by 5pm")

    elif text in ["my reminders", "list reminders"]:
        reminders = get_user_reminders(msg.from_user.phone)
        if not reminders:
            msg.reply("No reminders set!")
            return
        text = format_reminder_list(reminders)
        msg.reply(text)