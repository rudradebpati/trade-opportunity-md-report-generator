from pydantic import BaseModel, Field

class SectorInput(BaseModel):
    sector:str=Field(min_length=3, max_length=50)