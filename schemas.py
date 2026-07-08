from pydantic import BaseModel,ConfigDict,Field,EmailStr
from datetime import datetime
from enum import Enum


class SortField(str,Enum):
    title= "title"
    created_at= "created_at"


class NoteCreate(BaseModel):
    title: str | None= Field(min_length=3,max_length=40,default= None)
    content: str = Field(min_length=3)

class NoteResponse(BaseModel):
    id: int
    title: str | None
    content: str
    created_at: datetime
    last_updated: datetime | None

    is_pinned: bool = False
    is_archived: bool = False
    is_deleted: bool = False
    model_config = ConfigDict(from_attributes=True)

class UpdateNote(BaseModel):
    title: str | None= Field(min_length=3,max_length=40,default= None)
    content: str | None = Field(min_length=3,default= None)
    is_pinned: bool| None = None
    is_archived: bool | None = None 
    is_deleted: bool| None = None

class TrashNoteResponse(BaseModel):
    id: int
    title: str
    deleted_at: datetime
    model_config = ConfigDict(from_attributes=True)

class MessageResponse(BaseModel):
    message: str

    ########################  Users##################################



class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str = Field(min_length=8,max_length=128)

class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8,max_length=128)

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    is_verified: bool
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
