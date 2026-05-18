from datetime import datetime

from pydantic import BaseModel


class LinkBase(BaseModel):
    original_url: str


class LinkCreate(LinkBase): ...


class Link(LinkBase):
    id: int
    short_code: str
    created_at: datetime

    class Config:
        from_attributes = True
        json_encoders = {datetime: lambda dt: dt.isoformat()}
