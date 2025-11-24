from twilio.rest import Client
from app.core.config import settings


class WhatsAppService:
    def __init__(self):
        self.client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        self.from_number = f"whatsapp:{settings.TWILIO_PHONE_NUMBER}"
    
    async def send_message(self, to_phone: str, message_text: str) -> dict:
        try:
            message = self.client.messages.create(
                from_=self.from_number,
                body=message_text,
                to=to_phone
            )
            return {
                "success": True,
                "message_sid": message.sid,
                "status": message.status
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


async def handle_incoming_message(form_data: dict) -> dict:
    from_phone = form_data.get("From", "")
    message_body = form_data.get("Body", "")
    
    return {
        "status": "received",
        "from": from_phone,
        "message": message_body
    }


whatsapp_service = WhatsAppService()
