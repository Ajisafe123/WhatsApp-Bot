from datetime import datetime
from typing import Optional


def parse_phone_number(phone: str) -> str:
    cleaned = phone.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
    
    if not cleaned.startswith("+"):
        cleaned = "+" + cleaned
    
    return f"whatsapp:{cleaned}"


def format_message(user_name: Optional[str], message: str) -> str:
    greeting = f"Hi {user_name}! " if user_name else ""
    return greeting + message


def is_valid_datetime(dt_string: str) -> bool:
    try:
        datetime.fromisoformat(dt_string)
        return True
    except ValueError:
        return False
