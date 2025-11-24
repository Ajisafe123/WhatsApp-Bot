from celery import shared_task
from datetime import datetime, timedelta
from app.tasks.celery_app import celery_app
from app.services.reminder_service import ReminderService
from app.services.whatsapp import whatsapp_service


@celery_app.task
def send_reminder(reminder_id: str):
    pass


@celery_app.task
def schedule_reminder(reminder_id: str, scheduled_time: str):
    send_time = datetime.fromisoformat(scheduled_time)
    eta = send_time
    send_reminder.apply_async(args=[reminder_id], eta=eta)


@celery_app.task
def check_and_send_pending_reminders():
    pass


@celery_app.task
def cleanup_old_reminders():
    pass
