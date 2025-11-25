# handlers/callback_handler.py
from pywa.types.callback import CallbackSelection, CallbackButton, SectionList, Section
from utils.formatter import format_reminder_list
from services.reminder_service import get_user_reminders, delete_reminder
from utils.logger import logger

def register_callback_handlers(wa: "WhatsApp"):
    @wa.on_callback_selection()
    def handle_selection(client: "WhatsApp", cb: CallbackSelection):
        if cb.data == "list_reminders":
            reminders = get_user_reminders(cb.from_user.phone)
            text = format_reminder_list(reminders)
            cb.reply_text(text)

        elif cb.data.startswith("cancel_"):
            reminder_id = cb.data.split("_", 1)[1]
            delete_reminder(reminder_id)
            cb.reply_text("Reminder cancelled!", show_alert=True)

    @wa.on_callback_button()
    def handle_button(client: "WhatsApp", cb: CallbackButton):
        if cb.data == "set":
            cb.reply_text("Just type your reminder!\nExample: remind me to call dad by 6pm")
        elif cb.data == "list":
            reminders = get_user_reminders(cb.from_user.phone)
            if not reminders:
                cb.reply_text("No reminders yet!")
                return
            # Show list with cancel options
            sections = []
            for r in reminders:
                sections.append(
                    Section(
                        title=f"{r.task[:30]}...",
                        rows=[{"id": f"cancel_{r.id}", "title": "Cancel", "description": r.remind_time.strftime('%I:%M %p')}]
                    )
                )
            client.send_message(
                to=cb.from_user.phone,
                text="Select reminder to cancel:",
                footer="Reminder Bot",
                list_message=SectionList(
                    button_title="Cancel Reminder",
                    sections=sections
                )
            )