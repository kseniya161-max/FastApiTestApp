# schemas.py

from pydantic import BaseModel
from typing import List, Optional

class OperatorCreate(BaseModel):
    name: str
    is_active: bool = True
    max_active_leads: int = 5
    weight: int = 1

class OperatorResponse(OperatorCreate):
    id: int

    class Config:
        orm_mode = True

class SourceCreate(BaseModel):
    name: str

class SourceResponse(SourceCreate):
    id: int

    class Config:
        orm_mode = True

class ContactCreate(BaseModel):
    external_id: str
    source_id: int

class ContactResponse(ContactCreate):
    id: int

    class Config:
        orm_mode = True
