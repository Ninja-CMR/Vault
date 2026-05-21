from pydantic import BaseModel
from datetime import datetime

class GenerateMasterKeySchema(BaseModel):
    password: str
    force_regenerate: bool = False

class MasterKeyResponseSchema(BaseModel):
    master_key: str
    public_token: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class MasterKeyStatusSchema(BaseModel):
    has_master_key: bool
    public_token: str | None = None
    created_at: datetime | None = None

    class Config:
        from_attributes = True

class UnlockMasterKeySchema(BaseModel):
    password: str
