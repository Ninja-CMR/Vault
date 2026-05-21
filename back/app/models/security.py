from sqlalchemy import Column, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.database.database import Base

class MasterKey(Base):
    __tablename__ = "master_keys"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), unique=True, nullable=False)
    encrypted_master_key = Column(Text, nullable=False)
    public_token = Column(String(100), nullable=False)
    salt = Column(Text, nullable=False)
    kdf_algorithm = Column(String(50), nullable=False, default="pbkdf2_hmac")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # relationship
    user = relationship("User", backref="master_key_link", uselist=False)

    def __repr__(self):
        return f"<MasterKey(user_id={self.user_id})>"
