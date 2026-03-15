from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["school"]
students_col = db["students"]

print("Connected to MongoDB")

student = {
    "name": "Rahul",
    "age": 22,
    "course": "Data Engineering"
}

result = students_col.insert_one(student)

print("Inserted ID:", result.inserted_id)

students = [
    {"name": "Anita", "age": 21, "course": "AI"},
    {"name": "Kiran", "age": 23, "course": "Big Data"},
    {"name": "Meena", "age": 22, "course": "AI"}
]

students_col.insert_many(students)


for doc in students_col.find():
    print(doc)

print("Multiple students inserted")
