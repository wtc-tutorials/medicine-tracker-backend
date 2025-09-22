# models.py
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    medicines = relationship("Medicine", back_populates="owner")


class Medicine(Base):
    __tablename__ = "medicines"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    start_date = Column(Date)
    total_quantity = Column(Integer)
    daily_dosage = Column(Integer)  # simplification: once per day
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="medicines")
