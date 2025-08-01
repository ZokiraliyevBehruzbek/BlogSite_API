from pydantic import BaseModel

class WriteCategorySchema(BaseModel):
    name: str

class ReadCategorySchema(WriteCategorySchema):
    id: int