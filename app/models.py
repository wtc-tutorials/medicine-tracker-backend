from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey, Time
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # relationships
    medicines = relationship("Medicine", back_populates="owner", cascade="all, delete")


class Medicine(Base):
    __tablename__ = "medicines"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    name = Column(String, index=True, nullable=False)
    start_date = Column(Date, nullable=False)
    total_quantity = Column(Integer, nullable=False)
    daily_dosage = Column(Integer, nullable=False)

    # relationships
    owner = relationship("User", back_populates="medicines")
    dosages = relationship("Dosage", back_populates="medicine", cascade="all, delete")


class Dosage(Base):
    __tablename__ = "dosages"

    id = Column(Integer, primary_key=True, index=True)
    medicine_id = Column(
        Integer, ForeignKey("medicines.id", ondelete="CASCADE"), nullable=False
    )
    time_of_day = Column(Time, nullable=False)  # e.g., "08:00", "20:00"
    quantity = Column(Integer, nullable=False)

    # relationships
    medicine = relationship("Medicine", back_populates="dosages")
