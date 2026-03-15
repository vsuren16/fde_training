# ===============================
# SQLAlchemy Schema & MetaData
# ===============================
# MetaData acts as a central registry that keeps track of:
# - Table objects
# - Column definitions
# - Constraints (PK, FK, composite keys)
# - Relationships between tables
#
# Think of MetaData as a blueprint of your database schema in Python.
import os
from sqlalchemy import (
    MetaData, Table, Column,
    Integer, String, Numeric, DateTime, Enum,
    ForeignKey, ForeignKeyConstraint, Unicode, UnicodeText,
    create_engine, inspect
)

if os.path.exists("dev_02.db"):
    os.remove("dev_02.db")

# -------------------------------------------------
# Create a MetaData container
# -------------------------------------------------
# This object will hold all table definitions.
# Later, SQLAlchemy uses it to generate SQL.
metadata = MetaData()

# -------------------------------------------------
# Define a table using Table + Column objects
# -------------------------------------------------
# This defines a "user" table at the schema level.
# No database calls happen here yet.
user_table = Table(
    "user",                 # Table name in DB
    metadata,               # MetaData registry
    Column("id", Integer, primary_key=True),   # Primary key column
    Column("name", String),                     # Simple string column
    Column("fullname", String),                 # Another string column
)

# -------------------------------------------------
# Accessing table metadata
# -------------------------------------------------

# Table.name → returns the table name as a string
user_table.name

# Table.c → column collection (dict-like access)
# You can reference columns using attribute or key access
user_table.c.name

# Print all columns defined on the table
print(user_table.c)

# -------------------------------------------------
# Column-level metadata
# -------------------------------------------------

# Column name
user_table.c.name.name

# Column type (String, Integer, etc.)
user_table.c.name.type

# -------------------------------------------------
# Primary key information
# -------------------------------------------------

# Returns a PrimaryKeyConstraint object
user_table.primary_key
print(user_table.primary_key)
# -------------------------------------------------
# Generate a SQL SELECT statement
# -------------------------------------------------
# This does NOT execute the query.
# It only builds the SQL expression.
print(user_table.select())

# -------------------------------------------------
# Create a database engine
# -------------------------------------------------
# SQLite database stored in a local file "dev_02.db"
engine = create_engine("sqlite:///dev_02.db")

# -------------------------------------------------
# Emit CREATE TABLE statements
# -------------------------------------------------
# This actually talks to the database.
# All tables registered with metadata are created.
metadata.create_all(engine)

# -------------------------------------------------
# Demonstrating different column types
# -------------------------------------------------
fancy_table = Table(
    "fancy",
    metadata,
    Column("key", String(50), primary_key=True),  # VARCHAR with length
    Column("timestamp", DateTime),                # DateTime column
    Column("amount", Numeric(10, 2)),              # Decimal (precision, scale)
    Column(
        "type",
        Enum("a", "b", "c", name="fancy_type_enum")  # Enum constraint
    ),
)

# Create only this table (not all metadata tables)
fancy_table.create(engine)

# -------------------------------------------------
# Foreign key example (simple FK)
# -------------------------------------------------
addresses_table = Table(
    "address",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email_address", String(100), nullable=False),
    # ForeignKey creates a relationship to user.id
    Column("user_id", Integer, ForeignKey("user.id")),
)

# Emit CREATE TABLE for address
addresses_table.create(engine)

# -------------------------------------------------
# Composite primary key example
# -------------------------------------------------
story_table = Table(
    "story",
    metadata,
    Column("story_id", Integer, primary_key=True),
    Column("version_id", Integer, primary_key=True),
    Column("headline", Unicode(100), nullable=False),
    Column("body", UnicodeText),
)

# -------------------------------------------------
# Composite foreign key example
# -------------------------------------------------
published_table = Table(
    "published",
    metadata,
    Column("pub_id", Integer, primary_key=True),
    Column("pub_timestamp", DateTime, nullable=False),
    Column("story_id", Integer),
    Column("version_id", Integer),
    # ForeignKeyConstraint is required for multi-column FKs
    ForeignKeyConstraint(
        ["story_id", "version_id"],          # Local columns
        ["story.story_id", "story.version_id"]  # Referenced columns
    ),
)

# -------------------------------------------------
# create_all() behavior
# -------------------------------------------------
# Safe to call multiple times.
# SQLAlchemy skips tables that already exist.
metadata.create_all(engine)

# ===============================
# Reflection
# ===============================
# Reflection reads table definitions from an EXISTING database
# instead of defining them manually in code.

metadata2 = MetaData()

metadata2.reflect(bind=engine)
print(metadata2.tables.keys())


# ===============================
# Inspector
# ===============================
# Inspector provides database-level introspection utilities
# Useful for migrations, debugging, and tooling.

inspector = inspect(engine)

# List all tables in the database
inspector.get_table_names()
print("inspector:",inspector.get_table_names())
# Get column details for a table
inspector.get_columns("address")
print("inspector col:",inspector.get_columns("address"))
# Get foreign key details for a table
inspector.get_foreign_keys("address")
print("inspector fk:",inspector.get_foreign_keys("address"))