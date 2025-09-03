from pydantic import BaseModel, Field, field_validator
import re

class ContainerCreate(BaseModel):
    container_number: str = Field(..., min_length=11, max_length=11, example="CXXU7788345")
    cost: float = Field(..., gt=0, example=15000.00)

    @field_validator('container_number')
    @classmethod
    def check_format(cls, v):
        if not re.fullmatch(r"[A-Z]{3}U\d{7}", v):
            raise ValueError('Container number must be in format: AAAU1234567')
        return v

class ContainerResponse(BaseModel):
    id: int
    container_number: str
    cost: float