from services.email_service import get_gmail_service, extract_body
from queries.emails import upsert_email
from core.logger import get_logger
from email.utils import parsedate_to_datetime
from typing import Dict, Any

logger = get_logger(__name__)


def process_gmail_messages(user_id: str) -> Dict[str, Any]:
    """Process Gmail messages for a user and save them to database"""
    service = get_gmail_service(user_id)
    
    messages = service.users().messages().list(
        userId='me', maxResults=20
    ).execute().get('messages', [])

    if not messages:
        logger.error(f"No messages found for user {user_id}")
        return {
            'fetched': 0,
            'skipped': 0,
            'errors': 0,
            'error_ids': None
        }

    saved = []
    skipped = []
    errors = []

    for msg in messages:
        try:
            detail = service.users().messages().get(
                userId='me', id=msg['id'], format='full'
            ).execute()

            headers = {
                h['name']: h['value']
                for h in detail['payload']['headers']
            }

            body = extract_body(detail['payload'])

            email_data = {
                'user_id': user_id,
                'gmail_id': msg['id'],
                'subject': headers.get('Subject', '(no subject)'),
                'sender': headers.get('From', ''),
                'body': body[:5000],
                'thread_id': detail.get('threadId'),
                'received_at': parse_gmail_date(headers),
            }

            result = upsert_email(email_data)

            if result:
                saved.append(msg['id'])
            else:
                skipped.append(msg['id'])

        except Exception as e:
            logger.error(f"Failed to process message {msg['id']} for user {user_id}: {e}")
            errors.append(msg['id'])
            continue

    logger.info(f"User {user_id} — saved: {len(saved)}, skipped: {len(skipped)}, errors: {len(errors)}")

    return {
        'fetched': len(saved),
        'skipped': len(skipped),
        'errors': len(errors),
        'error_ids': errors if errors else None
    }


def parse_gmail_date(headers: dict) -> str:
    date_str = headers.get('Date', '')
    if date_str:
        try:
            return parsedate_to_datetime(date_str).isoformat()
        except Exception:
            pass