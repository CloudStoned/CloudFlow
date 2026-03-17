from pydantic import BaseModel
from typing import Optional

class ProviderTokenSchema(BaseModel):
    user_id: str
    access_token: str
    provider_refresh_token: Optional[str] = None