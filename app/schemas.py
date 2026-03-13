from datetime import datetime

from pydantic import BaseModel, HttpUrl, field_validator


class URLCreate(BaseModel):
    original_url: HttpUrl

    @field_validator("original_url", mode="before")
    @classmethod
    def normalize_url(cls, v: str) -> str:
        return str(v).rstrip("/")


class URLResponse(BaseModel):
    short_code: str
    short_url: str
    original_url: str
    created_at: datetime

    model_config = {"from_attributes": True}


class URLStats(BaseModel):
    short_code: str
    original_url: str
    access_count: int
    created_at: datetime
    is_active: bool

    model_config = {"from_attributes": True}