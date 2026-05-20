from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.generator import GeneratePasswordSchema, GeneratedPasswordResponseSchema
from app.services.generator_service import PasswordGeneratorService
from app.core.security import CurrentUserDep
from app.models.vault import Vault
from app.models.secret import Secret

router = APIRouter(
    prefix="/tools",
    tags=["Tools"]
)

@router.post("/password-generator", response_model=GeneratedPasswordResponseSchema)
def generate_password(
    options: GeneratePasswordSchema,
    current_user: CurrentUserDep,
    db: Session = Depends(get_db)
):
    """
    Générer un mot de passe sécurisé et incrémenter le compteur utilisateur.
    """
    result = PasswordGeneratorService.generate_password(options)
    
    # Incrémenter le compteur
    current_user.generated_passwords_count += 1
    db.commit()
    
    return result

@router.get("/stats")
def get_user_stats(
    current_user: CurrentUserDep,
    db: Session = Depends(get_db)
):
    """
    Récupérer les statistiques globales de l'utilisateur pour le dashboard.
    """
    vaults_count = db.query(Vault).filter(Vault.user_id == current_user.id).count()
    
    # Compter les secrets de tous les coffres de l'utilisateur
    secrets_count = db.query(Secret).join(Vault).filter(Vault.user_id == current_user.id).count()
    
    return {
        "vaults_count": vaults_count,
        "secrets_count": secrets_count,
        "generated_passwords_count": current_user.generated_passwords_count
    }
