from sqlalchemy import String, Integer
from sqlalchemy.orm import mapped_column, Mapped
from app.core.base_model import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int]= mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str]= mapped_column(String, nullable=False)
    hashed_password: Mapped[str]= mapped_column(String, nullable=False)
    email: Mapped[str]= mapped_column(String, nullable=False)
