from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.database import get_db
from app.schemas.vault import CreateVaultSchema, VaultResponseSchema
from app.services.vault_service import VaultService
from app.services.activity_service import ActivityLoggerService
from app.core.security import CurrentUserDep

router = APIRouter(
    prefix="/vaults",
    tags=["Vaults"]
)

@router.post("", response_model=VaultResponseSchema, status_code=status.HTTP_201_CREATED)
def create_vault(
    vault_data: CreateVaultSchema,
    current_user: CurrentUserDep,
    db: Session = Depends(get_db)
):
    """
    Créer un nouveau coffre pour l'utilisateur authentifié.
    """
    vault = VaultService.create_vault(db, current_user, vault_data)
    ActivityLoggerService.log_event(
        db, str(current_user.id), "vault_created", 
        resource_type="vault", resource_id=str(vault.id),
        metadata={"name": vault.name}
    )
    return vault

@router.get("", response_model=List[VaultResponseSchema])
def list_vaults(
    current_user: CurrentUserDep,
    db: Session = Depends(get_db)
):
    """
    Lister les coffres de l'utilisateur connecté.
    """
    return VaultService.get_user_vaults(db, current_user)
@router.get("/{vault_id}", response_model=VaultResponseSchema)
def get_vault(
    vault_id: str,
    current_user: CurrentUserDep,
    db: Session = Depends(get_db)
):
    """
    Obtenir les détails d'un coffre spécifique.
    """
    vault = VaultService.get_vault(db, current_user, vault_id)
    if not vault:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Coffre introuvable"
        )
    return vault

@router.put("/{vault_id}", response_model=VaultResponseSchema)
def update_vault(
    vault_id: str,
    vault_data: CreateVaultSchema,
    current_user: CurrentUserDep,
    db: Session = Depends(get_db)
):
    """
    Mettre à jour un coffre existant.
    """
    vault = VaultService.update_vault(db, current_user, vault_id, vault_data)
    if not vault:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Coffre introuvable"
        )
    ActivityLoggerService.log_event(
        db, str(current_user.id), "vault_updated", 
        resource_type="vault", resource_id=str(vault.id),
        metadata={"name": vault.name}
    )
    return vault

@router.delete("/{vault_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vault(
    vault_id: str,
    current_user: CurrentUserDep,
    db: Session = Depends(get_db)
):
    """
    Supprimer un coffre de l'utilisateur connecté.
    """
    success = VaultService.delete_vault(db, current_user, vault_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Coffre introuvable"
        )
    ActivityLoggerService.log_event(
        db, str(current_user.id), "vault_deleted", 
        resource_type="vault", resource_id=vault_id
    )
    return None
