from datetime import datetime

from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Slot(Base):
    """Model for available slots; supports FR-BKG-01, FR-BKG-06, ASM-01."""

    __tablename__ = "slots"

    id = Column(Integer, primary_key=True, index=True)
    slot_date = Column(Date, nullable=False, index=True)
    start_time = Column(String(5), nullable=False)
    package_code = Column(String(50), nullable=False)
    capacity = Column(Integer, nullable=False)
    remaining = Column(Integer, nullable=False)

    bookings = relationship("Booking", back_populates="slot")


class Booking(Base):
    """Model for user bookings; supports FR-BKG-02, FR-BKG-04, IF-HIS-01."""

    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    hn = Column(String(20), nullable=False, index=True)
    slot_id = Column(Integer, ForeignKey("slots.id"), nullable=False)
    booking_date = Column(Date, nullable=False, index=True)
    queue_no = Column(String(20), nullable=True)
    status = Column(String(20), nullable=False, default="confirmed")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    slot = relationship("Slot", back_populates="bookings")


class AuditLog(Base):
    """Audit log for access to booking data; supports DOM-PDPA-01."""

    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    actor_id = Column(String(64), nullable=False, index=True)
    action = Column(String(64), nullable=False)
    hn = Column(String(20), nullable=False, index=True)
    accessed_at = Column(DateTime, nullable=False, default=datetime.utcnow)
