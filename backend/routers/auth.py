from fastapi import APIRouter, Cookie, Depends
from core.dependencies import get_current_user
from services.auth_service import google_login, google_callback, logout

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get('/google')
async def google_login_endpoint(request):
    return await google_login(request)

@router.get('/callback')
async def google_callback_endpoint(request):
    return await google_callback(request)

@router.get('/me')
async def get_user_info(user_data = Depends(get_current_user)):
    return user_data

@router.post('/logout')
async def logout_endpoint():
    return await logout()
