from typing import Optional
from pydantic import BaseModel


class BlogsSchema(BaseModel):
    title: str
    description: str
    body: str
    status: Optional[str] = None
    # category: str