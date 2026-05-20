from pydantic import BaseModel, EmailStr, Field, field_validator
import re
from datetime import datetime
from typing import Optional
from uuid import UUID

class CreateUserSchema(BaseModel):
    email: EmailStr = Field(..., max_length=255)
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        if not re.search(r"[A-Z]", v):
            raise ValueError('Le mot de passe doit contenir au moins une lettre majuscule.')
        if not re.search(r"[a-z]", v):
            raise ValueError('Le mot de passe doit contenir au moins une lettre minuscule.')
        if not re.search(r"\d", v):
            raise ValueError('Le mot de passe doit contenir au moins un chiffre.')
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError('Le mot de passe doit contenir au moins un caractère spécial.')
        return v

class UserResponseSchema(BaseModel):
    id: str
    email: EmailStr
    username: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class LoginSchema(BaseModel):
    email: EmailStr
    password: str

class TokenSchema(BaseModel):
    access_token: str
    token_type: str
