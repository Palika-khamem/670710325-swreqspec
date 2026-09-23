import importlib

from sqlalchemy import create_engine, inspect


def test_T_01_db_schema_and_constraints():
    engine = create_engine("sqlite:///:memory:")

    migration = importlib.import_module("app.db.migrations.001_init")
    migration.upgrade(engine)

    inspector = inspect(engine)
    tables = set(inspector.get_table_names())

    assert {"slots", "bookings", "audit_logs"}.issubset(tables)

    bookings_columns = {col["name"] for col in inspector.get_columns("bookings")}
    assert "hn" in bookings_columns
    assert "national_id" not in bookings_columns

    audit_columns = {col["name"] for col in inspector.get_columns("audit_logs")}
    assert {"actor_id", "hn", "accessed_at"}.issubset(audit_columns)
