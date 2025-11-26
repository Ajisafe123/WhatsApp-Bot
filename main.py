import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
import os
from dotenv import load_dotenv
from handlers.message_handler import handle_incoming_message
from core.scheduler import start_scheduler
from utils.logger import logger

load_dotenv()

app = FastAPI(title="WhatsApp Reminder Bot")

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "your_verify_token")

start_scheduler()

@app.get("/webhook")
async def verify_webhook(request: Request):
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")
    
    if token == VERIFY_TOKEN:
        return PlainTextResponse(challenge)
    return PlainTextResponse("Invalid verification token", status_code=403)

@app.post("/webhook")
async def handle_webhook(request: Request):
    data = await request.json()
    
    try:
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
                            await handle_incoming_message(message, value)
                    
                    if statuses:
                        for status in statuses:
                            logger.info(f"Message status: {status}")
        
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
    
    return {"status": "ok"}

@app.get("/health")
async def health_check():
    return {"status": "running"}

if __name__ == "__main__":
    logger.info("Starting WhatsApp Reminder Bot")
    uvicorn.run(app, host="0.0.0.0", port=8000)
