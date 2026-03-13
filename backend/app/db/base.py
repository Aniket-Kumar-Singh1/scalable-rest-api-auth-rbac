"""
Import Base and all models so that Base.metadata.create_all() discovers every table.

main.py imports `Base` from here — do NOT import Base from database.py directly
in main.py, or the metadata may be empty.
"""

from app.db.database import Base  # noqa: F401

# Import every model module so their tables are registered on Base.metadata
from app.models.user_model import User  # noqa: F401
from app.models.task_model import Task  # noqa: F401