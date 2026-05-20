from sqlalchemy import Column, String, DateTime, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from app.database.database import Base
import enum

class SecretType(str, enum.Enum):
    LOGIN = "LOGIN"
    API_KEY = "API_KEY"
    TOKEN = "TOKEN"
    NOTE = "NOTE"

class Secret(Base):
    __tablename__ = "secrets"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    vault_id = Column(String, ForeignKey("vaults.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(150), nullable=False)
    type = Column(SQLEnum(SecretType), nullable=False)
    encrypted_value = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship with Vault
    vault = relationship("Vault", back_populates="secrets")

    def __repr__(self):
        return f"<Secret(title={self.title}, type={self.type})>"
