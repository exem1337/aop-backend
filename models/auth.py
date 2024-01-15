from pydantic import BaseModel, field_validator, EmailStr


class AuthSchema(BaseModel):
    email: EmailStr
    password: str
