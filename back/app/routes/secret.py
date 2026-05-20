from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.database import get_db
from app.schemas.secret import CreateSecretSchema, SecretResponseSchema, RevealSecretSchema
from app.services.secret_service import SecretService
from app.core.security import CurrentUserDep

router = APIRouter(
    prefix="/secrets",
    tags=["Secrets"]
)

@router.get("/all", response_model=List[SecretResponseSchema])
def list_all_secrets(
    current_user: CurrentUserDep,
    db: Session = Depends(get_db)
):
    """
    Lister tous les secrets de l'utilisateur (tous coffres confondus).
    """
    return SecretService.get_all_user_secrets(db, current_user)

@router.get("/{secret_id}", response_model=SecretResponseSchema)
def get_secret_metadata(
    secret_id: str,
    current_user: CurrentUserDep,
    db: Session = Depends(get_db)
):
    """
    Obtenir les métadonnées d'un secret.
    """
    return SecretService.get_secret_metadata(db, current_user, secret_id)

@router.get("/{secret_id}/reveal", response_model=RevealSecretSchema)
def reveal_secret(
    secret_id: str,
    current_user: CurrentUserDep,
    db: Session = Depends(get_db)
):
    """
    Obtenir la valeur chiffrée d'un secret pour déchiffrement client.
    """
    secret = SecretService.get_secret_metadata(db, current_user, secret_id)
    encrypted_val = SecretService.reveal_secret(db, current_user, secret_id)
    
    return {
        "id": secret.id,
        "title": secret.title,
        "type": secret.type,
        "encrypted_value": encrypted_val
    }

@router.delete("/{secret_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_secret(
    secret_id: str,
    current_user: CurrentUserDep,
    db: Session = Depends(get_db)
):
    """
    Supprimer un secret.
    """
    success = SecretService.delete_secret(db, current_user, secret_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Secret introuvable"
        )
    return None

# Vault-related secret routes (moved here or kept absolute)
@router.post("/vaults/{vault_id}", response_model=SecretResponseSchema, status_code=status.HTTP_201_CREATED)
def create_secret(
    vault_id: str,
    secret_data: CreateSecretSchema,
    current_user: CurrentUserDep,
    db: Session = Depends(get_db)
):
    """
    Ajouter un secret dans un coffre spécifié.
    """
    return SecretService.create_secret(db, current_user, vault_id, secret_data)

@router.get("/vaults/{vault_id}", response_model=List[SecretResponseSchema])
def list_vault_secrets(
    vault_id: str,
    current_user: CurrentUserDep,
    db: Session = Depends(get_db)
):
    """
    Lister les secrets d'un coffre spécifié.
    """
    return SecretService.get_vault_secrets(db, current_user, vault_id)
