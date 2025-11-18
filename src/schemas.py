from datetime import date
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict

class ContactBase(BaseModel):
    first_name: str = Field(max_length=20)
    last_name: str = Field(max_length=20)
    email: EmailStr
    phone_number: str = Field(max_length=15)
    birthday: date
    additional_data: Optional[str] = Field(default=None, max_length=50)

class ContactCreate(ContactBase):
    pass

class ContactUpdate(BaseModel):
    first_name: Optional[str] = Field(default=None, max_length=20)
    last_name: Optional[str] = Field(default=None, max_length=20)
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = Field(default=None, max_length=15)
    birthday: Optional[date] = None
    additional_data: Optional[str] = Field(default=None, max_length=50)

class ContactResponse(ContactBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)