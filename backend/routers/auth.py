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

class SaveTokenRequest(BaseModel):
    provider_token: str
    refresh_token: str
    user_id: str

@router.post("/token")
async def save_token(request: SaveTokenRequest):
    existing_user = supabase.table("user_tokens").select("*").eq("user_id", request.user_id).execute()
    
    if not existing_user.data:
        supabase.table("user_tokens").insert({
            "user_id": request.user_id,
            "access_token": request.provider_token,
            "refresh_token": request.refresh_token,
            "expires_at": (datetime.datetime.now() + timedelta(hours=1)).isoformat()
        }).execute()
    
    return {"success": True}