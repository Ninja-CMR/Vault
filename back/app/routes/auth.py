from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.user import CreateUserSchema, UserResponseSchema, LoginSchema, TokenSchema
from app.services.auth_service import UserCreationService
from app.core.security import create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/register", response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED)
def register(user_data: CreateUserSchema, db: Session = Depends(get_db)):
    """
    Créer un nouveau compte utilisateur Vault.
    """
    new_user = UserCreationService.create_user(db, user_data)
    return new_user

@router.post("/login", response_model=TokenSchema)
def login(login_data: LoginSchema, db: Session = Depends(get_db)):
    """
    Se connecter et obtenir un token JWT.
    """
    user = UserCreationService.authenticate_user(db, login_data.email, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
