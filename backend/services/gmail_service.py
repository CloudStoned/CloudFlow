from supabase import Client
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from repositories.user_tokens_repo import get_refresh_token
from core.config import get_settings

settings = get_settings()

def get_gmail_client(supabase: Client, user_id: str):

    refresh_token = get_refresh_token(supabase, user_id)

    creds = Credentials(
        None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=settings.GOOGLE_CLIENT_ID,
        client_secret=settings.GOOGLE_CLIENT_SECRET,
    )

    gmail = build("gmail", "v1", credentials=creds)

    return gmail


def test_gmail_connection(supabase: Client, user_id: str):

    gmail = get_gmail_client(supabase, user_id)

    response = gmail.users().labels().list(userId="me").execute()

    return response.get("labels", [])