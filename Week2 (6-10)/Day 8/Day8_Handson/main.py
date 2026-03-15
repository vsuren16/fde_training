import os
from sqlalchemy import (
    MetaData, Table, Column,
    Integer, String, Numeric, DateTime, Enum,
    ForeignKey, ForeignKeyConstraint, Unicode, UnicodeText,
    create_engine, inspect,text,select
)

# Remove existing database file for a clean run
if os.path.exists("dev_04.db"):
    os.remove("dev_04.db")

engine = create_engine("sqlite:///dev_04.db", echo=True)

with engine.connect() as conn:
    conn.execute(text("PRAGMA foreign_keys=ON"))

metadata = MetaData()

student_table = Table(
    "students",                 
    metadata,               
    Column("id", Integer, primary_key=True),   
    Column("name", String)                   
)
courses_table = Table(
    "courses",              
    metadata,              
    Column("id", Integer, primary_key=True),  
    Column("title", String)             
)



enrollments_table = Table(
    "enrollments",
    metadata,
    Column("student_id", Integer, ForeignKey("students.id")),
    Column("course_id", Integer, ForeignKey("courses.id"))
)

metadata.create_all(engine)

with engine.begin() as conn:
    conn.execute(text("insert into students(id,name) values (1,'John')"));
    conn.execute(text("insert into students(id,name) values (2,'Jane')"));
    conn.execute(text("insert into students(id,name) values (3,'Alice')"));
    conn.execute(text("insert into students(id,name) values (4,'Bob')"));

    conn.execute(text("insert into courses(id,title) values (1,'Mathematics')"));
    conn.execute(text("insert into courses(id,title) values (2,'Physics')"));

    conn.execute(text("insert into enrollments(student_id,course_id) values (1,1)"));
    conn.execute(text("insert into enrollments(student_id,course_id) values (2,1)"));
    conn.execute(text("insert into enrollments(student_id,course_id) values (3,2)"));
    conn.execute(text("insert into enrollments(student_id,course_id) values (4,2)"));

# Select and print all students
with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM students"))
    print("All students:")
    for row in result:
        print(row)

    # Get courses for a given student_id
    student_id = int(input("Enter student ID to get the course details: "))
    result = conn.execute(text("SELECT c.title FROM courses c JOIN enrollments e ON c.id = e.course_id WHERE e.student_id = :sid"), {"sid": student_id})
    print(f"Courses for student {student_id}:")
    for row in result:
        print(row[0])

    # Get students for a given course_id
    course_id = int(input("Enter course ID to get enrolled students: "))
    result = conn.execute(text("SELECT s.name FROM students s JOIN enrollments e ON s.id = e.student_id WHERE e.course_id = :cid"), {"cid": course_id})
    print(f"Students enrolled in course {course_id}:")
    for row in result:
        print(row[0])

inspector = inspect(engine)

# Print list of all table names
print("\nList of all table names:")
for table_name in inspector.get_table_names():
    print(table_name)


print("\nColumns for each table:")
for table_name in inspector.get_table_names():
    print(f"\nTable: {table_name}")
    columns = inspector.get_columns(table_name)
    for col in columns:
        print(f"  {col['name']}: {col['type']} (nullable: {col['nullable']})")

# Foreign keys for enrollments
print("\nForeign keys for enrollments table:")
fks = inspector.get_foreign_keys('enrollments')
for fk in fks:
    print(fk)


reflected_metadata = MetaData()


reflected_metadata.reflect(bind=engine)

students_reflected = reflected_metadata.tables['students']
with engine.connect() as conn:
    result = conn.execute(select(students_reflected))
    print("\nAll students from reflected metadata:")
    for row in result:
        print(row)

enrollments_reflected = reflected_metadata.tables['enrollments']
courses_reflected = reflected_metadata.tables['courses']
stmt = select(students_reflected.c.name, courses_reflected.c.title).select_from(
    students_reflected.join(enrollments_reflected, students_reflected.c.id == enrollments_reflected.c.student_id).join(
        courses_reflected, enrollments_reflected.c.course_id == courses_reflected.c.id
    )
)
with engine.connect() as conn:
    result = conn.execute(stmt)
    print("\nAll enrollments from reflected metadata:")
    for row in result:
        print(f"{row[0]} is enrolled in {row[1]}")