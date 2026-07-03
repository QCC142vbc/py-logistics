from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional


class Supplier(BaseModel):
    id: Optional[str] = None
    name: str = Field(..., min_length=1)
    email: EmailStr
    phone: str
    rating: float = Field(default=0.0, ge=0, le=5)
    is_active: bool = True
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
