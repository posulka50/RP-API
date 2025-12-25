from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

class CommunityCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    description: Optional[str] = Field(None, max_length=255)
    is_public: bool = Field(default=True)

class CommunityResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    owner_id: int
    is_public: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class CommunityProfileCreate(BaseModel):
    profile_name: str = Field(..., min_length=3, max_length=30)
    bio: Optional[str] = Field(None, max_length=255)

class CommunityProfileResponse(BaseModel):
    id: int
    user_id: int
    community_id: int
    profile_name: str
    role: str
    bio: Optional[str] = None
    is_active: bool
    joined_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
