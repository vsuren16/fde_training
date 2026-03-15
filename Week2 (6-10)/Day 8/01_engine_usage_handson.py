from sqlalchemy import create_engine, text
import os

if os.path.exists("dev_02.db"):
    os.remove("dev_02.db")

if os.path.exists("dev_01_handson.db"):
    os.remove("dev_01_handson.db")

# Create an Engine object representing the SQLite database and connection pool
engine = create_engine("sqlite:///dev_01_handson.db")

with engine.begin() as conn:
    conn.execute(text("""
        create table library (
            book_id integer primary key autoincrement,
            book_name varchar,
            book_desc varchar,
            book_price float
        )
    """))

    # Insert sample books
    conn.execute(text("insert into library(book_name,book_desc,book_price) values ('World War 3','About World War',100)"))
    conn.execute(text("insert into library(book_name,book_desc,book_price) values ('Tomorrow','About Life',55.55)"))

with engine.connect() as conn: 
    result = conn.execute(text("select * from  library"))
    print(result.fetchall())

with engine.connect() as conn: 
    try:
        conn.execute(text("insert into library(book_name,book_desc,book_price) values('Chinese Language','Chinese alphabets',1500)"))
        conn.commit()
        conn.close()
    except Exception as E:
        conn.rollback()
        conn.close()

with engine.connect() as conn: 
    result = conn.execute(text("select * from  library"))
    print(result.fetchall())