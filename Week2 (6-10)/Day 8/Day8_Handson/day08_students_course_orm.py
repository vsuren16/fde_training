from sqlalchemy import create_engine, String, select, Table, Column, Integer, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session

# Create a declarative Base
class Base(DeclarativeBase):
    pass

# Define the association table
enrollments_table = Table(
    'enrollments',
    Base.metadata,
    Column('student_id', Integer, ForeignKey('students.id')),
    Column('course_id', Integer, ForeignKey('courses.id'))
)

# Define ORM models
class Student(Base):
    __tablename__ = 'students'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))

    courses: Mapped[list["Course"]] = relationship(
        secondary=enrollments_table, back_populates='students'
    )

class Course(Base):
    __tablename__ = 'courses'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50))

    students: Mapped[list["Student"]] = relationship(
        secondary=enrollments_table, back_populates='courses'
    )

# Create engine (assuming the database is already created)
engine = create_engine("sqlite:///dev_04.db", echo=True)

# Create tables if not exist (but since reflected, they do)
Base.metadata.create_all(engine)

# Create a Session
with Session(engine) as session:

    student1 = Student(name='Alice_ORM')
    student2 = Student(name='Bob_ORM')
    course1 = Course(title='Math_ORM')
    course2 = Course(title='Science_ORM')

    session.add_all([student1, student2, course1, course2])
    session.commit()

    student1.courses.append(course1)
    student1.courses.append(course2)
    student2.courses.append(course1)

    session.commit()

    # Query: All students
    print("All students:")
    students = session.execute(select(Student)).scalars()
    for student in students:
        print(f"ID: {student.id}, Name: {student.name}")

    # All courses for one student using student.courses
    # Get the first student
    student = session.execute(select(Student).where(Student.name == 'Alice_ORM')).scalar_one()
    print(f"\nCourses for {student.name}:")
    for course in student.courses:
        print(course.title)

    # All students in one course using course.students
    course = session.execute(select(Course).where(Course.title == 'Math_ORM')).scalar_one()
    print(f"\nStudents in {course.title}:")
    for student in course.students:
        print(student.name)