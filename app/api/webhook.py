from fastapi import APIRouter, Request, status
from app.core.security import verify_twilio_request
from app.services.whatsapp import handle_incoming_message

router = APIRouter()


@router.post("/whatsapp")
async def whatsapp_webhook(request: Request):
    is_valid = await verify_twilio_request(request)
    if not is_valid:
        return {"error": "Invalid request"}, status.HTTP_403_FORBIDDEN
    form_data = await request.form()
    response = await handle_incoming_message(form_data)
    return response


@router.get("/status")
async def webhook_status():
    return {"status": "active"}
