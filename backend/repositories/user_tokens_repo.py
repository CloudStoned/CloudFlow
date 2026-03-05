from supabase import Client
from datetime import datetime

def save_refresh_token(supabase: Client, user_id: str, refresh_token: str):
    data = {
        "user_id": user_id,
        "google_refresh_token": refresh_token,
        "updated_at": datetime.now().isoformat()
    }

    response = supabase.table("user_tokens").upsert(data).execute()

    if not response.data:
        raise Exception("Failed to save refresh token")


def get_refresh_token(supabase: Client, user_id: str) -> str:
    response = (
        supabase.table("user_tokens")
        .select("google_refresh_token")
        .eq("user_id", user_id)
        .single()
        .execute()
    )

    token = response.data.get("google_refresh_token")

    if not token:
        raise Exception("No refresh token found")

    return token