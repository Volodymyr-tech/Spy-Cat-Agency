from pydantic import BaseModel, Field
from typing import List, Optional

from app.target.schemas import TargetBase


class MissionCreate(BaseModel):

    targets: List[TargetBase] = Field(..., min_length=1, max_length=3)

class MissionRead(BaseModel):
    id: int
    cat_id: Optional[int]
    is_completed: bool
    targets: List[TargetBase]

    class Config:
        from_attributes = True