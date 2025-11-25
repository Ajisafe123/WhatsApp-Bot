# core/client.py
from pywa import WhatsApp

wa_client = WhatsApp(
    phone_id="2349056453575",
    token="anything",           # can be anything
    verify_token="mysecret123", # ← THIS IS THE MISSING LINE
    server=None
)