from fastapi import APIRouter
from core.database import supabase
# AI Library
import json

router = APIRouter(prefix="/actions", tags=["actions"])
# AI Client

SYSTEM_PROMPT = """
You are an email analyzer. Read the email and return ONLY valid JSON:
{
  "requires_action": true or false,
  "tasks": ["task1", "task2", ...],
  "deadlines": ["deadline1", "deadline2", ...],
  "waiting_on_someone": true or false,
  "priority": "high" or "medium" or "low"
}
"""

@router.post('/analyze/{email_id}')
def analyze_email(email_id: str):
    email = supabase.table('emails').select('*') \
        .eq('id', email_id).single().execute().data
    # response = client.chat.completions.create(
    #     model='gpt-4o-mini',
    #     messages=[
    #         {'role': 'system', 'content': SYSTEM_PROMPT},
    #         {'role': 'user',   'content':
    #          f"Subject: {email['subject']}\n\n{email['body'][:2000]}"}
    #     ]
    # )
    # result = json.loads(response.choices[0].message.content)
    result = {
        "requires_action": True,
        "tasks": ["task1", "task2"],
        "deadlines": ["deadline1", "deadline2"],
        "waiting_on_someone": True,
        "priority": "high"
    }
    supabase.table('email_actions').upsert({
        'email_id': email_id,
        'user_id': email['user_id'],
        **result
    }).execute()
    return result
