from sqlalchemy import Column, String, DateTime, Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from app.database.database import Base

class Vault(Base):
    __tablename__ = "vaults"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship with User
    owner = relationship("User", back_populates="vaults")
    
    # Relationship with Secrets
    secrets = relationship("Secret", back_populates="vault", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint('user_id', 'name', name='_user_vault_name_uc'),
    )

    def __repr__(self):
        return f"<Vault(name={self.name}, owner={self.user_id})>"
