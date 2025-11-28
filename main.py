import os
import uvicorn
import asyncio
from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse, JSONResponse
from dotenv import load_dotenv
from handlers.message_handler import handle_incoming_message
from core.scheduler import start_scheduler
from handlers.callback_handlers import register_callback_handlers
from services.reminder_service import load_reminders
from services.notifier import send_reminder
from utils.logger import logger
from pywa import WhatsApp
from datetime import datetime
import pytz

load_dotenv()

app = FastAPI(title="WhatsApp Reminder Bot")
tz = pytz.timezone("Africa/Lagos")

wa = WhatsApp(
    phone_id=os.getenv("WHATSAPP_PHONE_ID"),
    token=os.getenv("WHATSAPP_TOKEN"),
    verify_token=os.getenv("VERIFY_TOKEN"),
    server=app
)

register_callback_handlers(wa)

async def reminder_loop():
    while True:
        now = datetime.now(tz)
        reminders = load_reminders()
        for r in reminders:
            if r.remind_time <= now and r.sent_count < r.repeat_count:
                send_reminder(r)
        await asyncio.sleep(60)

@app.on_event("startup")
def on_startup():
    start_scheduler()
    asyncio.create_task(reminder_loop())

@app.get("/webhook")
async def verify_webhook(request: Request):
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")
    if token == os.getenv("VERIFY_TOKEN"):
        return PlainTextResponse(challenge)
    return PlainTextResponse("Invalid verification token", status_code=403)

@app.post("/webhook")
async def handle_webhook(request: Request):
    try:
        data = await request.json()
    except Exception as e:
        logger.error(f"Invalid JSON payload: {e}")
        return JSONResponse({"error": "invalid json"}, status_code=400)

    if data.get("object") == "whatsapp_business_account":
        entries = data.get("entry", [])
        for entry in entries:
            changes = entry.get("changes", [])
            for change in changes:
                value = change.get("value", {})
                messages = value.get("messages", [])
                statuses = value.get("statuses", [])
                if messages:
                    for message in messages:
                        asyncio.create_task(handle_incoming_message(message, value))
                if statuses:
                    for status in statuses:
                        logger.info(f"Message status: {status}")
    return {"status": "ok"}

@app.get("/health")
async def health_check():
    return {"status": "running"}

@app.get("/ping")
async def ping():
    return PlainTextResponse("OK")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
