from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.database import get_db
from app.schemas.activity import ActivityLogResponseSchema, PaginatedActivityLogsResponseSchema
from app.services.activity_service import ActivityHistoryService
from app.core.security import get_current_user, CurrentUserDep
from app.models.user import User
import math

router = APIRouter(prefix="/activity", tags=["activity"])

@router.get("/logs", response_model=PaginatedActivityLogsResponseSchema)
async def get_activity_logs(
    page: int = 1,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Returns the activity logs for the authenticated user with pagination."""
    skip = (page - 1) * limit
    items, total = ActivityHistoryService.get_user_logs(db, current_user.id, limit, skip)
    
    return {
        "total": total,
        "items": items,
        "page": page,
        "limit": limit,
        "pages": math.ceil(total / limit) if total > 0 else 0
    }
