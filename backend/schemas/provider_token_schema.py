from pydantic import BaseModel
from typing import Optional

class ProviderTokenSchema(BaseModel):
    user_id: str
    google_access_token: str
    google_refresh_token: Optional[str] = None