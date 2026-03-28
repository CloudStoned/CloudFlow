from fastapi import APIRouter, HTTPException
from lib.email_processor import process_gmail_messages
from queries.emails import get_emails
from core.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/emails", tags=["emails"])

@router.post('/fetch/{user_id}')
def fetch_emails(user_id: str):
    try:
        return process_gmail_messages(user_id)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to process emails")

@router.post('/list/{user_id}')
def list_emails(user_id: str):
    try:
        return get_emails(user_id)
    except Exception as e:
        logger.error("Failed to list emails: %s", e)
        raise HTTPException(status_code=500, detail="Failed to list emails")