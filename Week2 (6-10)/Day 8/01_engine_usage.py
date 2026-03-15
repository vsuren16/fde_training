# Demonstrates basic usage of SQLAlchemy Engine with SQLite
# - Creates and connects to a SQLite database
# - Creates tables and inserts data using raw SQL
# - Executes queries and fetches results
# - Shows transaction management and result handling

from sqlalchemy import create_engine, text
import os

# Remove existing database file for a clean run
if os.path.exists("dev_01.db"):
    os.remove("dev_01.db")

# Create an Engine object representing the SQLite database and connection pool
engine = create_engine("sqlite:///dev_01.db")

# Create tables and insert data inside a transaction
with engine.begin() as conn:
    # Create 'employee' table
    conn.execute(text("""
        create table employee (
            emp_id integer primary key autoincrement,
            emp_name varchar
        )
    """))

    # Insert sample employees
    conn.execute(text("insert into employee(emp_name) values ('ed')"))
    conn.execute(text("insert into employee(emp_name) values ('jack')"))
    conn.execute(text("insert into employee(emp_name) values ('fred')"))

    # Create 'employee_of_month' table
    conn.execute(text("""
        create table employee_of_month (
            emp_id integer primary key,
            emp_name varchar
        )
    """))

# # Execute a parameterized SELECT query using a Connection
# with engine.connect() as conn:
#     result = conn.execute(
#         text("select emp_id, emp_name from employee where emp_id=:emp_id"),
#         {"emp_id": 3}
#     )
#     # Fetch one row from the result
#     row = result.fetchone()
#     print(row)

# # Iterate over all rows in the 'employee' table
# with engine.connect() as conn:
#     result = conn.execute(text("select * from employee"))
#     for row in result:
#         print(row)

# Fetch all rows at once using fetchall()
with engine.connect() as conn:
    result = conn.execute(text("select * from employee"))
    print(result.fetchall())

# Insert into 'employee_of_month' table inside a transaction
with engine.begin() as conn:
    conn.execute(
        text("insert into employee_of_month (emp_name) values (:emp_name)"),
        {"emp_name": "wendy"}
    )

with engine.connect() as conn:
    conn.execute(
        text("insert into employee_of_month (emp_name) values (:emp_name)"),
        {"emp_name": "NEW2 - wendy"}
    )
    conn.commit()

with engine.connect() as conn:
    result = conn.execute(text("select * from employee_of_month"))
    print(result.fetchall())


