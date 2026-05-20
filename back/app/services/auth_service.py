from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import CreateUserSchema, UserResponseSchema
from app.utils.security import hash_password, verify_password
from fastapi import HTTPException, status
from typing import Optional

class UserCreationService:
    @staticmethod
    def create_user(db: Session, user_data: CreateUserSchema) -> User:
        # ... (unchanged)
        # 1. Vérifier unicité email
        db_user = db.query(User).filter(User.email == user_data.email).first()
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Un utilisateur avec cet email existe déjà."
            )
        
        # 2. Hasher le mot de passe
        hashed_pw = hash_password(user_data.password)
        
        # 3. Créer l'utilisateur
        new_user = User(
            email=user_data.email,
            username=user_data.username,
            password_hash=hashed_pw
        )
        
        # 4. Sauvegarder en base
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        # 5. Retourner l'utilisateur créé
        return new_user

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user
