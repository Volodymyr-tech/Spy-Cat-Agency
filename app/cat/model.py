from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship

from app.core import Base


class Cat(Base):
    __tablename__ = "cats"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    years_experience = Column(Integer)
    breed = Column(String)
    salary = Column(Float)
    mission = relationship("Mission", back_populates="cat", uselist=False)