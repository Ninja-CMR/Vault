from sqlalchemy.orm import Session
from app.models.vault import Vault
from app.models.user import User
from app.schemas.vault import CreateVaultSchema
from fastapi import HTTPException, status
from typing import List, Optional

class VaultService:
    @staticmethod
    def create_vault(db: Session, user: User, vault_data: CreateVaultSchema) -> Vault:
        # 1. Vérifier l'unicité du nom pour cet utilisateur
        existing_vault = db.query(Vault).filter(
            Vault.user_id == user.id,
            Vault.name == vault_data.name
        ).first()
        
        if existing_vault:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Un coffre nommé '{vault_data.name}' existe déjà pour cet utilisateur."
            )
        
        # 2. Créer le coffre
        new_vault = Vault(
            user_id=user.id,
            name=vault_data.name,
            description=vault_data.description
        )
        
        # 3. Sauvegarder
        db.add(new_vault)
        db.commit()
        db.refresh(new_vault)
        
        return new_vault

    @staticmethod
    def get_user_vaults(db: Session, user: User) -> List[Vault]:
        return db.query(Vault).filter(Vault.user_id == user.id).all()

    @staticmethod
    def get_vault(db: Session, user: User, vault_id: str) -> Optional[Vault]:
        return db.query(Vault).filter(
            Vault.id == vault_id,
            Vault.user_id == user.id
        ).first()

    @staticmethod
    def delete_vault(db: Session, user: User, vault_id: str) -> bool:
        vault = VaultService.get_vault(db, user, vault_id)
        if not vault:
            return False
            
        db.delete(vault)
        db.commit()
        return True
