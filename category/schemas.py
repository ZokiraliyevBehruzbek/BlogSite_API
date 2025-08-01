from pydantic import BaseModel

class WriteCategorySchema(BaseModel):
    name: str