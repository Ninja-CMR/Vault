from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID

class CreateVaultSchema(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=500)

class VaultResponseSchema(BaseModel):
    id: str
    name: str
    description: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
