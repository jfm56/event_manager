from builtins import ValueError, any, bool, str
from pydantic import BaseModel, EmailStr, HttpUrl, Field, constr, validator, root_validator
from typing import Optional, List
from datetime import datetime
from enum import Enum
from uuid import UUID
import re


from app.utils.nickname_gen import generate_nickname

class UserRole(str, Enum):
    ANONYMOUS = "ANONYMOUS"
    AUTHENTICATED = "AUTHENTICATED"
    MANAGER = "MANAGER"
    ADMIN = "ADMIN"

def validate_url(url: Optional[str]) -> Optional[str]:
    if url is None:
        return url
    url_regex = r'^https?:\/\/[^\s/$.?#].[^\s]*$'
    if not re.match(url_regex, url):
        raise ValueError('Invalid URL format')
    return url

class UserBase(BaseModel):
    username: EmailStr = Field(..., example="john_doe_123")
    nickname: Optional[str] = Field(None, min_length=3, pattern=r'^[\w-]+$', example=generate_nickname())
    first_name: Optional[str] = Field(None, example="John")
    last_name: Optional[str] = Field(None, example="Doe")
    bio: Optional[str] = Field(None, example="Experienced software developer specializing in web applications.")
    profile_picture_url: Optional[str] = Field(None, example="https://example.com/profiles/john.jpg")
    linkedin_profile_url: Optional[str] =Field(None, example="https://linkedin.com/in/johndoe")
    github_profile_url: Optional[str] = Field(None, example="https://github.com/johndoe")

    _validate_urls = validator('profile_picture_url', 'linkedin_profile_url', 'github_profile_url', pre=True, allow_reuse=True)(validate_url)
 
    class Config:
        from_attributes = True

class UserUpdate(UserBase):
    email: Optional[EmailStr] = Field(None, example="john.doe@example.com")
    nickname: Optional[str] = Field(None, min_length=3, pattern=r'^[\w-]+$', example="john_doe123")
    first_name: Optional[str] = Field(None, example="John")
    last_name: Optional[str] = Field(None, example="Doe")
    bio: Optional[str] = Field(None, example="Experienced software developer specializing in web applications.")
    profile_picture_url: Optional[str] = Field(None, example="https://example.com/profiles/john.jpg")
    linkedin_profile_url: Optional[str] =Field(None, example="https://linkedin.com/in/johndoe")
    github_profile_url: Optional[str] = Field(None, example="https://github.com/johndoe")

    @root_validator(pre=True)
    def check_at_least_one_value(cls, values):
        if not any(values.values()):
            raise ValueError("At least one field must be provided for update")
        return values

class UserResponse(BaseModel):
    id: UUID
    username: EmailStr
    nickname: Optional[constr(min_length=3, pattern=r'^[A-Za-z0-9_-]+$')] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    bio: Optional[str] = None
    profile_picture_url: Optional[HttpUrl] = None
    linkedin_profile_url: Optional[HttpUrl] = None
    github_profile_url: Optional[HttpUrl] = None
    role: UserRole = UserRole.AUTHENTICATED
    is_professional: bool = False
    created_at: datetime
    last_login_at: datetime

class LoginRequest(BaseModel):
    username: str = Field(..., example="john_doe_123")
    password: str = Field(..., example="Secure*1234")

class UserBase(BaseModel):
    username: EmailStr
    nickname: Optional[constr(min_length=3, pattern=r'^[A-Za-z0-9_-]+$')] = None
    first_name: str
    last_name: str
    bio: Optional[str] = None
    profile_picture_url: Optional[HttpUrl] = None
    linkedin_profile_url: Optional[HttpUrl] = None
    github_profile_url: Optional[HttpUrl] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    nickname: Optional[constr(min_length=3, pattern=r'^[A-Za-z0-9_]+$')] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    bio: Optional[str] = None
    profile_picture_url: Optional[HttpUrl] = None
    linkedin_profile_url: Optional[HttpUrl] = None
    github_profile_url: Optional[HttpUrl] = None

class UserListResponse(BaseModel):
    items: List[UserResponse] = Field(
        ...,
        example=[
            {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "username": "john.doe@example.com",
                "nickname": "jdoe42",
                "first_name": "John",
                "last_name": "Doe",
                "bio": "Experienced developer",
                "role": "AUTHENTICATED",
                "is_professional": False,
                "profile_picture_url": "https://example.com/profiles/john.jpg",
                "linkedin_profile_url": "https://linkedin.com/in/johndoe",
                "github_profile_url": "https://github.com/johndoe",
                "created_at": "2025-04-21T01:34:30.268953",
                "last_login_at": "2025-04-21T01:34:30.268951"
            }
        ]
    )
    total: int = Field(..., example=100)
    page: int  = Field(..., example=1)
    size: int  = Field(..., example=10)
