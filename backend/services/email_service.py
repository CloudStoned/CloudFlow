from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from queries.user_tokens import get_user_tokens, update_user_tokens
from core.logger import get_logger
from core.config import get_settings
from fastapi import HTTPException
import base64

logger = get_logger(__name__)
settings = get_settings()


def get_gmail_service(user_id: str):
    token_data = get_user_tokens(user_id)
    if not token_data:
        logger.error(f"User {user_id} not found")
        raise HTTPException(status_code=404, detail="User tokens not found")

    creds = Credentials(
        token=token_data.get("google_access_token"),
        refresh_token=token_data.get("google_refresh_token"),
        token_uri="https://oauth2.googleapis.com/token",
        client_id=settings.GOOGLE_CLIENT_ID,
        client_secret=settings.GOOGLE_CLIENT_SECRET,
    )

    if creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
            update_user_tokens(user_id, {
                "google_access_token": creds.token
            })
            logger.info(f"Refreshed access token for user {user_id}")
        except Exception as e:
            logger.error(f"Failed to refresh token for user {user_id}: {e}")
            raise HTTPException(status_code=401, detail="Token refresh failed, re-authenticate required")

    return build("gmail", "v1", credentials=creds)


def extract_body(payload: dict) -> str:
    if 'parts' in payload:
        for part in payload['parts']:
            if part['mimeType'].startswith('multipart'):
                result = extract_body(part)
                if result:
                    return result
            if part['mimeType'] == 'text/plain':
                data = part.get('body', {}).get('data', '')
                if data:
                    return base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')

    data = payload.get('body', {}).get('data', '')
    if data:
        return base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')

    return ''