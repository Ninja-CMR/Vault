from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.security import (
    GenerateMasterKeySchema, 
    MasterKeyStatusSchema, 
    MasterKeyResponseSchema,
    UnlockMasterKeySchema
)
from app.services.security_service import MasterKeyService
from app.services.activity_service import ActivityLoggerService
from app.core.security import CurrentUserDep

router = APIRouter(
    prefix="/security",
    tags=["Security"]
)

@router.post("/master-key/generate", response_model=MasterKeyResponseSchema, status_code=status.HTTP_201_CREATED)
def generate_master_key(
    data: GenerateMasterKeySchema,
    current_user: CurrentUserDep,
    db: Session = Depends(get_db)
):
    """
    Génère ou régénère une master key pour l'utilisateur.
    """
    db_mk, mk, pt = MasterKeyService.create_master_key(
        db, current_user.id, data.password, force_regenerate=data.force_regenerate
    )
    ActivityLoggerService.log_event(
        db, str(current_user.id), "master_key_generated", 
        status="success", metadata={"public_token": pt}
    )
    return {"master_key": mk, "public_token": pt, "created_at": db_mk.created_at}

@router.post("/master-key/unlock", response_model=MasterKeyResponseSchema)
def unlock_master_key(
    data: UnlockMasterKeySchema,
    current_user: CurrentUserDep,
    db: Session = Depends(get_db)
):
    """
    Déverrouille la master key de l'utilisateur.
    """
    mk, pt = MasterKeyService.unlock_master_key(db, current_user.id, data.password)
    db_mk = MasterKeyService.get_user_master_key_status(db, current_user.id)
    ActivityLoggerService.log_event(
        db, str(current_user.id), "master_key_unlocked", 
        status="success", metadata={"public_token": pt}
    )
    return {"master_key": mk, "public_token": pt, "created_at": db_mk.created_at}

@router.get("/master-key/status", response_model=MasterKeyStatusSchema)
def get_master_key_status(
    current_user: CurrentUserDep,
    db: Session = Depends(get_db)
):
    """
    Vérifie si l'utilisateur possède une master key.
    """
    mk = MasterKeyService.get_user_master_key_status(db, current_user.id)
    return {
        "has_master_key": mk is not None,
        "public_token": mk.public_token if mk else None,
        "created_at": mk.created_at if mk else None
    }
