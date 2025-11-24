from fastapi import FastAPI
from app.api import webhook, reminders

app = FastAPI(
    title="WhatsApp Reminder Bot",
    description="A reminder bot using WhatsApp via Twilio",
    version="1.0.0"
)

app.include_router(webhook.router, prefix="/webhook", tags=["webhook"])
app.include_router(reminders.router, prefix="/reminders", tags=["reminders"])


@app.get("/")
def read_root():
    return {"status": "ok", "message": "WhatsApp Reminder Bot is running"}


@app.on_event("startup")
async def startup_event():
    print("WhatsApp Reminder Bot started")


@app.on_event("shutdown")
async def shutdown_event():
    print("WhatsApp Reminder Bot stopped")
