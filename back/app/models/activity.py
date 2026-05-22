from sqlalchemy import Column, String, DateTime, JSON, ForeignKey
import uuid
from datetime import datetime
from app.database.database import Base

class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=True)
    organization_id = Column(String, nullable=True) # For future Org support
    
    event_type = Column(String(100), nullable=False)
    resource_type = Column(String(100), nullable=True)
    resource_id = Column(String, nullable=True)
    
    ip_address = Column(String(255), nullable=True)
    device_info = Column(String(500), nullable=True)
    status = Column(String(50), default="success")
    
    metadata_json = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
