from core.database import supabase
from typing import Optional, Dict, Any


def get_user_tokens(user_id: str) -> Optional[Dict[str, Any]]:
    """Get user tokens by user_id"""
    result = supabase.table("user_tokens").select("*").eq("user_id", user_id).single().execute()
    return result.data if result.data else None


def update_user_tokens(user_id: str, token_data: Dict[str, Any]) -> bool:
    """Update user tokens"""
    result = supabase.table("user_tokens").update(token_data).eq("user_id", user_id).execute()
    return bool(result.data)


def insert_user_tokens(token_data: Dict[str, Any]) -> bool:
    """Insert new user tokens"""
    result = supabase.table("user_tokens").insert(token_data).execute()
    return bool(result.data)


def check_user_tokens_exist(user_id: str) -> bool:
    """Check if user tokens exist"""
    result = supabase.table("user_tokens").select("user_id").eq("user_id", user_id).execute()
    return bool(result.data)
