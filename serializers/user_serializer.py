from pydantic import BaseModel, Field, EmailStr
class UserBase(BaseModel):
   first_name: str = Field(..., min_length=1, max_length=50)
   last_name: str = Field(..., min_length=1, max_length=50)
   email: str = Field(..., pattern=r"^[^@]+@[^@]+\.[^@]+$")
   mobile_number: str = Field(..., pattern=r"^\+?\d{10,15}$")
class UserCreate(UserBase):
   password: str = Field(..., min_length=6)
class UserUpdate(BaseModel):
   first_name: str
   last_name: str
   email: EmailStr
   mobile_number: str
   password: str
class UserResponse(UserBase):
   id: int
   class Config:
       from_attributes = True
