from pydantic import BaseModel, Field, validate_email, EmailStr, ConfigDict
from typing import Annotated, Optional, Literal
from datetime import datetime

class UserAddByAdminSchema(BaseModel):
    username: Annotated[str, Field(..., min_length=2, max_length=30, description="Username for login")]
    password: Annotated[str, Field(..., min_length=8, max_length=128, description="Password for login")]
    role: Annotated[Literal["admin", "user"], Field(default="user")]


class UserLoginSchema(BaseModel):
    username: str
    password: str


class UserReadSchema(BaseModel):
    id: int = Field(description="User ID")
    username: str = Field(description="Username")
    is_active: bool = Field(description="Is active")
    role: str = Field(description="Role")
    create_at: datetime = Field(description="Created at")

    model_config = ConfigDict(from_attributes=True)


class UserUpdateSchema(BaseModel):
    username: Annotated[Optional[str], Field(None, min_length=2, max_length=30, description="New username")]
    password: Annotated[Optional[str], Field(None, min_length=8, max_length=128, description="New password")]
    is_active: Annotated[Optional[bool], Field(None)]

    model_config = ConfigDict(extra="forbid")



