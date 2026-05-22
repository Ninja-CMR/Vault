from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional, Dict, Any, List

class ActivityLogResponseSchema(BaseModel):
    id: str
    event_type: str
    resource_type: Optional[str]
    resource_id: Optional[str]
    status: str
    created_at: datetime
    metadata_json: Optional[Dict[str, Any]]

    class Config:
        from_attributes = True

class PaginatedActivityLogsResponseSchema(BaseModel):
    total: int
    items: List[ActivityLogResponseSchema]
    page: int
    limit: int
    pages: int
