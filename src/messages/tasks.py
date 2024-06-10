import json
import logging

import requests

from src.celery import celery, SessionLocal
from src.messages.models import MessageDB


@celery.task
def send_telegram_message(message, chat_id, bot_id):
    telegram_url = f"https://api.telegram.org/{bot_id}/sendMessage"
    data = {"chat_id": chat_id, "text": message}

    response = requests.post(telegram_url, data)

    return json.loads(response.text)


@celery.task
def save_response_from_telegram(message_id):
    db = SessionLocal()

    try:
        # Retrieve the message from the database
        message = db.query(MessageDB).filter(MessageDB.id == message_id).one()

        # Call send_telegram_message synchronously
        resp = send_telegram_message(message.message, message.chat_id, message.bot_token)

        # Update the message response and commit changes
        message.response = resp
        db.commit()

        return "OK"
    except Exception as e:
        logging.warning(e)
        # Handle exceptions
        db.rollback()
        raise e
    finally:
        # Close the database connection
        db.close()
