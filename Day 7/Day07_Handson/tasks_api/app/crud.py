from datetime import datetime, timedelta
from pymongo import MongoClient
from bson import ObjectId

# Database connection
client = MongoClient("mongodb://localhost:27017")
db = client.tasks_db
tasks_col = db.tasks


#create_task
def create_task(payload: dict) -> dict:
    result = tasks_col.insert_one(payload)
    return {"_id": str(result.inserted_id), **payload}

#list task 
def list_tasks(status: str | None = None, priority: str | None = None) -> list[dict]:
    query = {}
    if status is not None:
        query["status"] = status
    if priority is not None:
        query["priority"] = priority
    tasks = list(tasks_col.find(query))
    for task in tasks:
        task["_id"] = str(task["_id"])
    return tasks

#get_task
def get_task(task_id: str) -> dict | None:
    task = tasks_col.find_one({"_id": ObjectId(task_id)})
    if task:
        task["_id"] = str(task["_id"])
    return task

#update_task
def update_task(task_id: str, payload: dict) -> dict | None:
    result = tasks_col.update_one({"_id": ObjectId(task_id)}, {"$set": payload})
    if result.matched_count == 0:
        return None
    return get_task(task_id)

#delete_task
def delete_task(task_id: str) -> bool:
    result = tasks_col.delete_one({"_id": ObjectId(task_id)})
    return result.deleted_count > 0


