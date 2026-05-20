from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class SecretType(str, Enum):
    LOGIN = "LOGIN"
    API_KEY = "API_KEY"
    TOKEN = "TOKEN"
    NOTE = "NOTE"

class CreateSecretSchema(BaseModel):
    title: str = Field(..., min_length=2, max_length=150)
    type: SecretType
    encrypted_value: str = Field(..., description="Le bloc de données déjà chiffré par le client")
    description: Optional[str] = Field(None, max_length=500)

class SecretResponseSchema(BaseModel):
    id: str
    vault_id: str
    title: str
    type: SecretType
    description: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

class RevealSecretSchema(BaseModel):
    id: str
    title: str
    type: SecretType
    encrypted_value: str

    class Config:
        from_attributes = True
