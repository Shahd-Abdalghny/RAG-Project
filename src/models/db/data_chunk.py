from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId

class DataChunk(BaseModel):
    _id: Optional[ObjectId] 
    chunk_text: str = Field(..., min_length=1)
    chunk_metadata: dict
    chunk_project_id: ObjectId
    chunk_order: int = Field(..., ge=0)
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True