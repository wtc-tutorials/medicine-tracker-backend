# app/models.py
import uuid
from datetime import datetime
from sqlalchemy import (
    Column,
    String,
    DateTime,
    Enum,
    Date,
    Time,
    Integer,
    ForeignKey,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
from enum import Enum as PyEnum

Base = declarative_base()


class GenderEnum(PyEnum):
    MALE = "male"
    FEMALE = "female"


class User(Base):
    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(120), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    date_of_birth = Column(Date, nullable=True)
    gender = Column(
        Enum(GenderEnum, name="gender_enum", create_type=False), nullable=True
    )
    created_at = Column(DateTime, default=datetime.utcnow)

    medicines = relationship(
        "Medicine", back_populates="user", cascade="all, delete-orphan"
    )


class Medicine(Base):
    __tablename__ = "medicines"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    start_date = Column(Date, nullable=False)
    total_quantity = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="medicines")
    dosages = relationship(
        "Dosage", back_populates="medicine", cascade="all, delete-orphan"
    )


class Dosage(Base):
    __tablename__ = "dosages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    medicine_id = Column(
        UUID(as_uuid=True),
        ForeignKey("medicines.id", ondelete="CASCADE"),
        nullable=False,
    )
    time_of_day = Column(Time, nullable=False)
    quantity = Column(Integer, nullable=False)

    medicine = relationship("Medicine", back_populates="dosages")
