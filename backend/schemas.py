from datetime import datetime

from pydantic import BaseModel

from models import UserRole


class LinkBase(BaseModel):
    original_url: str


class LinkCreate(LinkBase):
    custom_short_code: str | None = None


class Link(LinkBase):
    id: int
    short_code: str
    created_at: datetime

    class Config:
        from_attributes = True
        json_encoders = {datetime: lambda dt: dt.isoformat()}


class UserCreate(BaseModel):
    email: str
    password: str


class LinkResponse(BaseModel):
    id: int
    original_url: str
    short_code: str
    created_at: datetime

    class Config:
        from_attributes = True


class UserInDB(BaseModel):
    id: str
    email: str
    hashed_password: str
    role: UserRole

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    id: str
    email: str
    role: UserRole

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    email: str
    password: str
