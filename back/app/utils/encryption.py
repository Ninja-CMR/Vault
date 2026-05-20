import os
from cryptography.fernet import Fernet
import base64

# Configuration de la clé de chiffrement
# En production, cette clé doit être stockée dans une variable d'environnement sécurisée.
ENCRYPTION_KEY = os.getenv("VAULT_ENCRYPTION_KEY")

if not ENCRYPTION_KEY:
    # Pour le développement, on génère une clé si elle n'existe pas
    # ATTENTION: En production, cela entraînerait la perte d'accès aux données si la clé change.
    ENCRYPTION_KEY = Fernet.generate_key().decode()
    os.environ["VAULT_ENCRYPTION_KEY"] = ENCRYPTION_KEY

class EncryptionService:
    @staticmethod
    def encrypt(text: str) -> str:
        """Chiffre une chaîne de caractères en utilisant Fernet."""
        f = Fernet(ENCRYPTION_KEY.encode())
        return f.encrypt(text.encode()).decode()

    @staticmethod
    def decrypt(encrypted_text: str) -> str:
        """Déchiffre une chaîne de caractères en utilisant Fernet."""
        f = Fernet(ENCRYPTION_KEY.encode())
        return f.decrypt(encrypted_text.encode()).decode()
