from fastapi import APIRouter
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from core.database import supabase
from core.logger import get_logger
from core.config import get_settings
import base64
import datetime

logger = get_logger(__name__)
settings = get_settings()

router = APIRouter(prefix="/emails", tags=["emails"])

def get_gmail_service(user_id: str):
  result = supabase.table("user_tokens").select("*").eq("user_id", user_id).single().execute()
  if not result.data:
    logger.error(f"User {user_id} not found")
    return None
  
  token_data = result.data
  creds = Credentials(
    token = token_data.get("access_token"),
    refresh_token = token_data.get("refresh_token"),
    token_uri = "https://oauth2.googleapis.com/token",
    client_id = settings.GOOGLE_CLIENT_ID,
    client_secret = settings.GOOGLE_CLIENT_SECRET,
  )
  
  return build("gmail", "v1", credentials=creds)

@router.post('/fetch/{user_id}')
def fetch_emails(user_id: str):
    service = get_gmail_service(user_id)
    messages = service.users().messages().list(
        userId='me', maxResults=20
    ).execute().get('messages', [])
 
    saved = []
    for msg in messages:
        detail = service.users().messages().get(
            userId='me', id=msg['id'], format='full'
        ).execute()
        headers = {h['name']: h['value']
                   for h in detail['payload']['headers']}
        body = ''
        if 'data' in detail['payload'].get('body', {}):
            body = base64.urlsafe_b64decode(
                detail['payload']['body']['data']
            ).decode('utf-8', errors='ignore')
        supabase.table('emails').insert({
            'user_id': user_id,
            'gmail_id': msg['id'],
            'subject': headers.get('Subject', ''),
            'sender': headers.get('From', ''),
            'body': body[:5000],
            'thread_id': detail.get('threadId'),
            'received_at': datetime.datetime.now().isoformat()
        }).execute()
        saved.append(msg['id'])
    return {'fetched': len(saved)}
