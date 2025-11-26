from core.client import wa_client
from services.reminder_service import add_reminder, list_reminders, delete_reminder
from utils.parser import parse_reminder_command
from utils.formatter import format_reminders
from utils.logger import logger
from config.settings import ALLOWED_USERS
from models.reminder import Reminder

async def handle_incoming_message(message: dict, metadata: dict):
    from_number = message.get("from", "")
    message_type = message.get("type", "text")
    message_id = message.get("id", "")

    logger.info(f"Received message from {from_number}: {message}")

    if from_number not in ALLOWED_USERS:
        logger.warning(f"Unauthorized user: {from_number} not in {ALLOWED_USERS}")
        wa_client.send_message(from_number, "You are not authorized to use this bot.")
        return

    if message_type == "text":
        text = message.get("text", {}).get("body", "").strip().lower()
        logger.info(f"Processing text message: {text}")
        await process_text_message(from_number, text, message_id)


async def process_text_message(from_number: str, text: str, message_id: str):
    if text in ["hi", "hello", "menu", "start"]:
        menu_message = """👋 *Welcome to Reminder Bot!*

I help you set reminders and manage your tasks.

*Commands:*
📌 *remind me to [task] by [time]*  
   Example: remind me to study by 3pm

📋 *my reminders*  
   View all your reminders

🗑️ *delete reminder [number]*  
   Example: delete reminder 1

Type any command to get started! 🚀"""

        wa_client.send_message(from_number, menu_message)

    elif "remind me" in text:
        parsed_list = parse_reminder_command(text, from_number)
        if parsed_list:
            responses = []
            for parsed in parsed_list:
                repeat_count = parsed.get("repeat_count", 1)
                interval = parsed.get("interval_minutes", 0)

                reminder = Reminder(
                    from_number,
                    parsed["task"],
                    parsed["remind_time"],
                    repeat_count=repeat_count,
                    interval_minutes=interval
                )
                add_reminder(reminder)
                responses.append(
                    f"✅ Reminder set!\n📌 {reminder.task}\n⏰ {parsed['time']}\n🔁 Will repeat {reminder.repeat_count} time(s)"
                )

            wa_client.send_message(from_number, "\n\n".join(responses))
        else:
            wa_client.send_message(
                from_number,
                "❌ Invalid format.\nTry: remind me to study by 3pm"
            )

    elif text in ["my reminders", "list reminders"]:
        reminders = list_reminders(from_number)
        if not reminders:
            wa_client.send_message(from_number, "No reminders set.")
            return

        formatted = format_reminders(reminders)
        wa_client.send_message(from_number, formatted)

    elif text.startswith("delete reminder"):
        parts = text.split()
        if len(parts) >= 3:
            try:
                index = int(parts[2]) - 1
                delete_reminder(from_number, index)
                wa_client.send_message(from_number, "✅ Reminder deleted.")
            except (ValueError, IndexError):
                wa_client.send_message(from_number, "Invalid reminder number.")
        else:
            wa_client.send_message(from_number, "Invalid reminder command.")

    else:
        wa_client.send_message(from_number, "I don't understand. Type 'hi' for menu.")
