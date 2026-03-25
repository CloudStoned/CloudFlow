from fastapi import APIRouter, Request
from core.dependencies import get_current_user
from fastapi import Depends
from services.auth_service import google_login, google_callback, logout as logout_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["auth"])

@router.get('/google')
async def handle_google_login(request: Request):
    return await google_login(request)

@router.get('/callback')
async def handle_google_callback(request: Request):
    return await google_callback(request)

@router.get('/me')
async def get_user_info(user_data = Depends(get_current_user)):
    return user_data

@router.post("/logout")
async def handle_logout():
    return await logout_service()