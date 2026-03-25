from fastapi import Request, HTTPException
from fastapi.responses import RedirectResponse
from core.database import supabase
from core.config import get_settings
from core.logger import get_logger
import datetime
from datetime import timedelta
from schemas.provider_token_schema import ProviderTokenSchema

logger = get_logger(__name__)
settings = get_settings()

FRONTEND_URL = "http://localhost:3000"


async def google_login(request: Request):
    """Initiate Google OAuth login flow."""
    response = supabase.auth.sign_in_with_oauth({
        "provider": "google",
        "options": {
            "redirect_to": "http://localhost:8000/auth/callback",
            "scopes": "openid email profile https://www.googleapis.com/auth/gmail.readonly",
        }
    })
    return RedirectResponse(url=response.url)


async def google_callback(request: Request):
    """Handle Google OAuth callback."""
    code = request.query_params.get("code")
    if not code:
        return RedirectResponse(url=f"{FRONTEND_URL}/login?error=missing_code")

    try:
        session = supabase.auth.exchange_code_for_session({"auth_code": code})

        supabase_access_token = session.session.access_token
        supabase_refresh_token = session.session.refresh_token

        google_access_token = session.session.provider_token
        google_refresh_token = session.session.provider_refresh_token

        user_id = session.user.id

        await save_provider_token(
            ProviderTokenSchema(
                user_id=user_id,
                access_token=google_access_token,
                provider_refresh_token=google_refresh_token
            )
        )

        response = RedirectResponse(url=f"{FRONTEND_URL}/dashboard")
        IS_PRODUCTION = settings.ENV == "production"

        response.set_cookie(
            "access_token",
            supabase_access_token,
            httponly=True,
            secure=IS_PRODUCTION,
            samesite="lax",
            max_age=3600
        )

        response.set_cookie(
            "refresh_token",
            supabase_refresh_token,
            httponly=True,
            secure=IS_PRODUCTION,
            samesite="lax",
            max_age=60 * 60 * 24 * 30
        )

        return response

    except Exception as e:
        logger.error(f"OAuth callback error: {e}")
        return RedirectResponse(url=f"{FRONTEND_URL}/login?error=auth_failed")


async def save_provider_token(data: ProviderTokenSchema):
    """Save provider token to database."""
    try:
        token_data = {
            "user_id": data.user_id,
            "google_access_token": data.access_token,
            "expires_at": (datetime.datetime.now() + timedelta(hours=1)).isoformat()
        }

        if data.provider_refresh_token:
            token_data["google_refresh_token"] = data.provider_refresh_token

        existing = supabase.table("user_tokens") \
            .select("user_id") \
            .eq("user_id", data.user_id) \
            .execute()

        if not existing.data:
            supabase.table("user_tokens").insert(token_data).execute()
        else:
            supabase.table("user_tokens").update(token_data).eq("user_id", data.user_id).execute()

        logger.info(f"Provider token saved for user {data.user_id}")

    except Exception as e:
        logger.error(f"Failed to save provider token: {e}")


async def logout():
    """Handle user logout."""
    response = RedirectResponse(url=f"{FRONTEND_URL}/login")
    response.delete_cookie("access_token", path="/")
    response.delete_cookie("refresh_token", path="/")
    
    supabase.auth.sign_out()
    
    return response
