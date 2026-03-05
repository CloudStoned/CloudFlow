from fastapi import APIRouter, Depends, Request
from supabase import Client
from services.gmail_service import test_gmail_connection
from core.database import get_supabase
from core.logger import get_logger

router = APIRouter(prefix="/gmail", tags=["gmail"])
logger = get_logger(__name__)

@router.get("/test/{user_id}")
def test_connection(user_id: str, supabase: Client = Depends(get_supabase)):
    return test_gmail_connection(supabase, user_id)

@router.post("/save-refresh-token")
async def gmail_token(req: Request):
    data = await req.json()
    
    return {"message": data}