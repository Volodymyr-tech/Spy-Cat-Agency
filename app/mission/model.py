from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship

from app.core import Base


class Mission(Base):
    __tablename__ = "missions"
    id = Column(Integer, primary_key=True)
    cat_id = Column(Integer, ForeignKey("cats.id"), nullable=True)
    is_completed = Column(Boolean, default=False)

    cat = relationship("Cat", back_populates="mission")
    targets = relationship("Target", back_populates="mission", cascade="all, delete-orphan")

