from typing import List, Optional

from pydantic import BaseModel, Field


class TargetCreate(BaseModel):
    name: str
    country: str
    notes: Optional[str] = ""


class MissionCreate(BaseModel):
    targets: List[TargetCreate] = Field(..., min_items=1, max_items=3)