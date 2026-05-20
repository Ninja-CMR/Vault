from sqlalchemy.orm import Session
from app.models.secret import Secret, SecretType
from app.models.vault import Vault
from app.models.user import User
from app.schemas.secret import CreateSecretSchema
from app.utils.encryption import EncryptionService
from fastapi import HTTPException, status
from typing import List, Optional

class SecretService:
    @staticmethod
    def create_secret(db: Session, user: User, vault_id: str, secret_data: CreateSecretSchema) -> Secret:
        # 1. Vérifier que le coffre appartient à l'utilisateur
        vault = db.query(Vault).filter(Vault.id == vault_id, Vault.user_id == user.id).first()
        if not vault:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Coffre introuvable ou accès refusé."
            )
        
        # 2. Créer le secret avec la valeur déjà chiffrée par le client
        new_secret = Secret(
            vault_id=vault_id,
            title=secret_data.title,
            type=secret_data.type,
            encrypted_value=secret_data.encrypted_value,
            description=secret_data.description
        )
        
        # 3. Sauvegarder
        db.add(new_secret)
        db.commit()
        db.refresh(new_secret)
        
        return new_secret

    @staticmethod
    def get_vault_secrets(db: Session, user: User, vault_id: str) -> List[Secret]:
        # Vérifier accès au coffre
        vault = db.query(Vault).filter(Vault.id == vault_id, Vault.user_id == user.id).first()
        if not vault:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Coffre introuvable ou accès refusé."
            )
        return db.query(Secret).filter(Secret.vault_id == vault_id).all()

    @staticmethod
    def get_secret_metadata(db: Session, user: User, secret_id: str) -> Secret:
        secret = db.query(Secret).join(Vault).filter(
            Secret.id == secret_id,
            Vault.user_id == user.id
        ).first()
        
        if not secret:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Secret introuvable ou accès refusé."
            )
        return secret

    @staticmethod
    def get_all_user_secrets(db: Session, user: User) -> List[Secret]:
        return db.query(Secret).join(Vault).filter(Vault.user_id == user.id).order_by(Secret.created_at.desc()).all()

    @staticmethod
    def reveal_secret(db: Session, user: User, secret_id: str) -> str:
        secret = SecretService.get_secret_metadata(db, user, secret_id)
        # On retourne simplement la valeur chiffrée, le client s'occupe du déchiffrement
        return secret.encrypted_value

    @staticmethod
    def delete_secret(db: Session, user: User, secret_id: str) -> bool:
        secret = db.query(Secret).join(Vault).filter(
            Secret.id == secret_id,
            Vault.user_id == user.id
        ).first()
        
        if not secret:
            return False
            
        db.delete(secret)
        db.commit()
        return True
