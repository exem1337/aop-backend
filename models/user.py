from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, EmailStr

from enums.color import EColorSchema
from enums.role import ERole
from enums.status import EStatus


class User(BaseModel):
    id: int
    name: str
    last_name: str
    middle_name: str
    role: ERole
    email: EmailStr
    password: bytes
    color_schema: Optional[EColorSchema]
    status: Optional[EStatus]


class AddUser(BaseModel):
    email: EmailStr
    password: str
    role: str
    name: str
    last_name: str
    middle_name: str
    status: str

    class Config:
        from_attributes = True
