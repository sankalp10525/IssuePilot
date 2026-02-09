"""
Celery tasks for notifications.
"""
from celery import shared_task

from apps.notifications.selectors import outbox_pending_messages
from apps.notifications.services import process_outbox_message


@shared_task
def process_outbox_messages():
    """Process pending outbox messages."""
    messages = outbox_pending_messages(limit=100)
    
    for message in messages:
        process_outbox_message(message=message)
    
    return f"Processed {len(messages)} messages"


@shared_task
def send_daily_digest():
    """Send daily digest emails (scaffold)."""
    # TODO: Implement daily digest logic
    pass
