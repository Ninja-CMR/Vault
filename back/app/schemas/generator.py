from pydantic import BaseModel, Field

class GeneratePasswordSchema(BaseModel):
    length: int = Field(16, ge=8, le=128)
    include_uppercase: bool = True
    include_lowercase: bool = True
    include_numbers: bool = True
    include_symbols: bool = True

class GeneratedPasswordResponseSchema(BaseModel):
    password: str
    strength: str
    entropy_score: float
