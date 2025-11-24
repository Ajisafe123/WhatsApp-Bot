from fastapi import Request
from twilio.request_validator import RequestValidator
from app.core.config import settings


async def verify_twilio_request(request: Request) -> bool:
    validator = RequestValidator(settings.TWILIO_AUTH_TOKEN)
    
    url = str(request.url)
    method = request.method
    form_data = await request.form()
    params = dict(form_data)
    signature = request.headers.get("X-Twilio-Signature", "")
    
    is_valid = validator.validate(url, method, params, signature)
    
    return is_valid
