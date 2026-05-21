import hashlib
import os
import secrets
import base64
from cryptography.fernet import Fernet
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.security import MasterKey
from app.models.user import User

class KeyDerivationService:
    @staticmethod
    def generate_salt(length: int = 16) -> str:
        return base64.b64encode(os.urandom(length)).decode('utf-8')

    @staticmethod
    def derive_key(password: str, salt: str, iterations: int = 100000) -> str:
        """Derive a 32-byte key using PBKDF2-HMAC-SHA256."""
        salt_bytes = base64.b64decode(salt)
        derived = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt_bytes,
            iterations,
            dklen=32
        )
        return base64.urlsafe_b64encode(derived).decode('utf-8')

class MasterKeyService:
    @staticmethod
    def generate_master_key() -> str:
        """Generates a random 32-byte master key."""
        return secrets.token_urlsafe(32)

    @staticmethod
    def encrypt_master_key(master_key: str, kek: str) -> str:
        """Encrypt the master key using the Key Encryption Key (derived from password)."""
        f = Fernet(kek.encode())
        return f.encrypt(master_key.encode()).decode()

    @staticmethod
    def decrypt_master_key(encrypted_master_key: str, kek: str) -> str:
        """Decrypt the master key using the Key Encryption Key."""
        f = Fernet(kek.encode())
        return f.decrypt(encrypted_master_key.encode()).decode()

    @staticmethod
    def get_user_master_key_status(db: Session, user_id: str):
        return db.query(MasterKey).filter(MasterKey.user_id == user_id).first()

    @staticmethod
    def generate_public_token() -> str:
        """Generates a human-friendly public token."""
        return f"VAT-{secrets.token_hex(4).upper()}-{secrets.token_hex(4).upper()}"

    @classmethod
    def unlock_master_key(cls, db: Session, user_id: str, password: str):
        db_mk = cls.get_user_master_key_status(db, user_id)
        if not db_mk:
            raise HTTPException(status_code=404, detail="Master key not found")
            
        kek = KeyDerivationService.derive_key(password, db_mk.salt)
        try:
            mk = cls.decrypt_master_key(db_mk.encrypted_master_key, kek)
            return mk, db_mk.public_token
        except Exception:
            raise HTTPException(status_code=401, detail="Incorrect password")

    @classmethod
    def create_master_key(cls, db: Session, user_id: str, password: str, force_regenerate: bool = False):
        # 1. Handle existing key
        existing_mk = cls.get_user_master_key_status(db, user_id)
        if existing_mk:
            if force_regenerate:
                db.delete(existing_mk)
                db.commit()
            else:
                raise HTTPException(status_code=400, detail="Une master key existe déjà pour cet utilisateur.")

        # 2. Generate salt and derive KEK
        salt = KeyDerivationService.generate_salt()
        kek = KeyDerivationService.derive_key(password, salt)
        
        # 2. Generate actual Master Key and Public Token
        mk = cls.generate_master_key()
        pt = cls.generate_public_token()
        
        # 3. Encrypt MK with KEK
        encrypted_mk = cls.encrypt_master_key(mk, kek)
        
        # 4. Save to DB
        db_mk = MasterKey(
            user_id=user_id,
            encrypted_master_key=encrypted_mk,
            public_token=pt,
            salt=salt,
            kdf_algorithm="pbkdf2_hmac"
        )
        db.add(db_mk)
        db.commit()
        db.refresh(db_mk)
        return db_mk, mk, pt
