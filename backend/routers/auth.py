from fastapi import APIRouter
from google_auth_oauthlib.flow import Flow
from core.database import supabase
from core.config import get_settings
from core.logger import get_logger

logger = get_logger(__name__)

settings = get_settings()

router = APIRouter(prefix="/auth", tags=["auth"])

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
]

def get_flow():
  return Flow.from_client_config(
    {"web":{
      "client_id": settings.GOOGLE_CLIENT_ID,
      "client_secret": settings.GOOGLE_CLIENT_SECRET,
      "auth_uri": "https://accounts.google.com/o/oauth2/auth",
      "token_uri": "https://oauth2.googleapis.com/token",
    }},
    scopes=SCOPES,
    redirect_uri=settings.FRONTEND_URL + "/auth/callback"
  )

@router.get("/google")
async def google_login():
  try:
    flow = get_flow()
    auth_url, _ = flow.authorization_url(prompt="consent", access_type="offline")
    return {"auth_url": auth_url}
  except Exception as e:
    logger.error(f"Error in google_login: {e}")
    raise e

@router.post("/callback")
async def google_callback(code: str, user_id: str):
  try:
    flow = get_flow()
    flow.fetch_token(code=code)
    creds = flow.credentials
    supabase.table("user_tokens").upsert({
      "user_id": user_id,
      "access_token": creds.token,
      "refresh_token": creds.refresh_token,
      "expires_at": creds.expiry.isoformat()
    }).execute()
    return {"success": True}
  except Exception as e:
    logger.error(f"Error in google_callback: {e}")
    raise e
