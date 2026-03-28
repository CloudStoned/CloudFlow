from fastapi import APIRouter, HTTPException
from lib.email_processor import process_gmail_messages

router = APIRouter(prefix="/emails", tags=["emails"])


@router.post('/fetch/{user_id}')
def fetch_emails(user_id: str):
    try:
        return process_gmail_messages(user_id)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to process emails")