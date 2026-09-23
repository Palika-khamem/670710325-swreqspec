from sqlalchemy import MetaData, Table, Column, Date, DateTime, ForeignKey, Integer, String, create_engine


def upgrade(engine):
    """Create core schema for booking, slot availability, and audit access; supports CON-TECH-01, DOM-PDPA-01, IF-HIS-01."""
    metadata = MetaData()

    Table(
        "slots",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("slot_date", Date, nullable=False),
        Column("start_time", String(5), nullable=False),
        Column("package_code", String(50), nullable=False),
        Column("capacity", Integer, nullable=False),
        Column("remaining", Integer, nullable=False),
    )

    Table(
        "bookings",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("hn", String(20), nullable=False),
        Column("slot_id", Integer, ForeignKey("slots.id"), nullable=False),
        Column("booking_date", Date, nullable=False),
        Column("queue_no", String(20), nullable=True),
        Column("status", String(20), nullable=False, default="confirmed"),
        Column("created_at", DateTime, nullable=False),
    )

    Table(
        "audit_logs",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("actor_id", String(64), nullable=False),
        Column("action", String(64), nullable=False),
        Column("hn", String(20), nullable=False),
        Column("accessed_at", DateTime, nullable=False),
    )

    metadata.create_all(bind=engine)
