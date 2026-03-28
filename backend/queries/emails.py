from core.database import supabase
from typing import Optional, Dict, Any


def upsert_email(email_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Upsert an email record - update if exists, insert if not"""
    gmail_id = email_data.get('gmail_id')
    if not gmail_id:
        return None
    
    existing = supabase.table('emails').select('*').eq('gmail_id', gmail_id).execute()
    
    if existing.data:
        result = supabase.table('emails').update(email_data).eq('gmail_id', gmail_id).execute()
        return result.data if result.data else None
    else:
        result = supabase.table('emails').insert(email_data).execute()
        return result.data if result.data else None

def get_emails(user_id: str):
    return supabase.table('emails').select('*').eq('user_id', user_id).execute()