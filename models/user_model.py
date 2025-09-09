from sqlalchemy import Column, Integer, String
from .base_model import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    mobile_number = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
