from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from fastapi import Form

class UserRegister(BaseModel):
    first_name: str = Field(..., min_length=3, max_length=100)
    last_name: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)
    confirm_password: str = Field(..., min_length=6)

    @classmethod
    def as_form(
        cls,
        first_name: str = Form(...),
        last_name: str = Form(...),
        email: EmailStr = Form(...),
        password: str = Form(...),
        confirm_password: str = Form(...),
    ):
        return cls(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            confirm_password=confirm_password,
        )

class UserUpdate(BaseModel):
    first_name: Optional[str] = None 
    last_name: Optional[str] = None 
    photo_url: Optional[str] = None 

    @classmethod
    def as_form(
        cls,
        first_name: str = Form(...),
        last_name: str = Form(...),
        photo_url: str = Form(...)
    ):
        return cls(
            first_name=first_name,
            last_name=last_name,
            photo_url=photo_url
        )


class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    photo_url: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

    @classmethod
    def as_form(
        cls,
        email: str = Form(...),
        password: str = Form(...)
    ):
        return cls(
            email=email,
            password=password
        )