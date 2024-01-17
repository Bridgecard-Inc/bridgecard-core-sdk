from typing import Any, Dict, Optional
from pydantic import BaseModel


class WebhookEventSession(BaseModel):
    issuing_app_id: str
    header: Optional[Dict[str, Any]]
    event: str
    data: Dict[str, Any]
    environment: str