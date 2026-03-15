import os
from sqlalchemy import (
    MetaData, Table, Column,
    Integer, String, Numeric, DateTime, Enum,
    ForeignKey, ForeignKeyConstraint, Unicode, UnicodeText,
    create_engine, inspect
)

if os.path.exists("dev_02_handson.db"):
    os.remove("dev_02_handson.db")

engine = create_engine("sqlite:///dev_02_handson.db")

metadata_1 = MetaData()


book_table = Table(
    "book",
    metadata_1,
    Column("book_id", Integer, primary_key=True),  # VARCHAR with length
    Column("book_name",  String(50)),                # DateTime column
    Column("book_desc",  String(50)),              # Decimal (precision, scale)
    Column("book_publishdate", DateTime),              # Decimal (precision, scale)
)

# Create only this table (not all metadata tables)
book_table.create(engine)

publish_table = Table(
    "publish",
    metadata_1,
    Column("publish_id", Numeric, primary_key=True),  # VARCHAR with length
    Column("book_name",  String(50)),                # DateTime column
    Column("date", DateTime),              # Decimal (precision, scale)
    Column("book_id", Integer, ForeignKey("book.book_id")),
)

# Create only this table (not all metadata tables)
publish_table.create(engine)