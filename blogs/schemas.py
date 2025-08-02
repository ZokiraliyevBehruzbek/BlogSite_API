from typing import Optional
from pydantic import BaseModel


class BlogsSchema(BaseModel):
    title: str
    description: str
    body: str
    status: Optional[str] = None
    category_id: int 


class UpdateSchema(BlogsSchema):
    title: Optional[str] = None
    # category_id: Optional[int] = None
    description: Optional[str] = None
    body: Optional[str] = None

class UpdateStatus(BaseModel):
    status: str