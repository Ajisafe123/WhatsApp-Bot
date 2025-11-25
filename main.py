# main.py
from core.client import wa_client
from handlers.message_handler import handle_message
from handlers.callback_handler import register_callback_handlers
from utils.logger import logger

wa_client.on_message(handle_message)
register_callback_handlers(wa_client)

if __name__ == "__main__":
    logger.info("Starting WhatsApp Reminder Bot...")
    logger.info("Scan QR with +2349056453575")
    wa_client.run_with_server(port=8000)