from pydantic import BaseModel



class CatCreate(BaseModel):
    name: str
    years_experience: int
    breed: str
    salary: float


