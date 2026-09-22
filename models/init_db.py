from models.database import engine, Base
from models import models  # noqa: F401 — import registers the table classes on Base.metadata

# create_all() scans every class that inherits from Base and issues
# CREATE TABLE for any that don not already exist in the target database.
# Safe to re-run: existing tables are left untouched.
Base.metadata.create_all(bind=engine)

print("Tables created.")