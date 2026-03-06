from fastapi import APIRouter
from core.database import supabase
from core.config import get_settings
from core.logger import get_logger
import datetime
from datetime import timedelta
from pydantic import BaseModel

logger = get_logger(__name__)

settings = get_settings()

router = APIRouter(prefix="/auth", tags=["auth"])

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
]

class LinkGmailRequest(BaseModel):
    access_token: str
    refresh_token: str
    user_id: str

@router.post("/link-gmail")
async def link_gmail(request: LinkGmailRequest):
    supabase.table("user_tokens").upsert({
        "user_id": request.user_id,
        "access_token": request.access_token,
        "refresh_token": request.refresh_token,
        "expires_at": (datetime.datetime.now() + timedelta(hours=1)).isoformat()
    }).execute()
    return {"success": True}