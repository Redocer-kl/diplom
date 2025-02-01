from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: str

class UserOut(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

class TaskCreate(BaseModel):
    title: str
    description: str
    user_id: int

class TaskOut(BaseModel):
    id: int
    title: str
    description: str
    completed: bool
    created_at: datetime
    user_id: int

class TaskUpdate(BaseModel):
    completed: bool