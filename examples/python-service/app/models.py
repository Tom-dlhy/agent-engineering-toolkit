from pydantic import BaseModel, ConfigDict, Field

class ResourceResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: int = Field(gt=0)
    name: str = Field(min_length=1, max_length=200)
