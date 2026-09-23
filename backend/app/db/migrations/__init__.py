import importlib


def upgrade(engine):
    """Load and run the current migration; supports CON-TECH-01."""

    module = importlib.import_module("app.db.migrations.001_init")
    return module.upgrade(engine)
