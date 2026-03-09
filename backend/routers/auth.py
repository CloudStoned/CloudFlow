from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from core.database import supabase
from core.config import get_settings
from core.logger import get_logger
from core.oauth_config import oauth
import datetime
from datetime import timedelta
from pydantic import BaseModel
from typing import Optional

logger = get_logger(__name__)

settings = get_settings()

router = APIRouter(prefix="/auth", tags=["auth"])

class SaveTokenRequest(BaseModel):
    provider_token: str
    provider_refresh_token: Optional[str] = None
    user_id: str

@router.get('/google')
async def google_login(request: Request):
    redirect_uri = 'http://localhost:8000/auth/callback'
    return await oauth.google.authorize_redirect(
        request,
        redirect_uri,
    )

@router.get('/callback')
async def google_callback(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
        user_info = token.get('userinfo')

        if not user_info:
            user_info = await oauth.google.parse_id_token(request, token)
        
        code = request.query_params.get('code')
        if not code:
            return RedirectResponse(url=f"{settings.FRONTEND_URL}/login?error=no_code")

        provider_token = token.get('access_token')
        provider_refresh_token = token.get('refresh_token')

        try:
            auth_response = supabase.auth.admin.create_user({
                "email": user_info['email'],
                "email_confirm": True,
                "user_metadata": {
                    "name": user_info.get('name', ''),
                    "picture": user_info.get('picture', '')
                }
            })
            user_id = auth_response.user.id
        except Exception:
            user = supabase.auth.admin.get_user_by_email(user_info['email'])
            user_id = user.user.id

        if provider_token:
            await save_token(SaveTokenRequest(
                provider_token=provider_token,
                provider_refresh_token=provider_refresh_token,
                user_id=user_id
            ))
        
        return RedirectResponse(url=f"{settings.FRONTEND_URL}/dashboard")
        
    except Exception as e:
        logger.error(f"OAuth callback error: {str(e)}")
        return RedirectResponse(url=f"{settings.FRONTEND_URL}/login?error=oauth_failed")

async def save_token(request: SaveTokenRequest):
    existing_token = supabase.table("user_tokens").select("*").eq("user_id", request.user_id).execute()
    
    token_data = {
        "user_id": request.user_id,
        "access_token": request.provider_token,
        "expires_at": (datetime.datetime.now() + timedelta(hours=1)).isoformat()
    }

    if request.provider_refresh_token:
        token_data["refresh_token"] = request.provider_refresh_token

    if not existing_token.data:
        supabase.table("user_tokens").insert(token_data).execute()
    else:
        supabase.table("user_tokens").update(token_data).eq("user_id", request.user_id).execute()
    
    return {"success": True}