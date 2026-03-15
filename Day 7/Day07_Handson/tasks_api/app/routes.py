from fastapi import APIRouter, HTTPException
from .models import TaskCreate, TaskUpdate, TaskResponse
from .crud import create_task, list_tasks, get_task, update_task, delete_task

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/", response_model=TaskResponse)
async def create_task_route(payload: TaskCreate):
    task = create_task(payload.dict())
    return task

@router.get("/", response_model=list[TaskResponse])
async def list_tasks_route(status: str | None = None, priority: str | None = None):
    tasks = list_tasks(status=status, priority=priority)
    return tasks

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task_route(task_id: str):
    task = get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=TaskResponse)
async def update_task_route(task_id: str, payload: TaskUpdate):
    updated = update_task(task_id, {k: v for k, v in payload.dict().items() if v is not None})
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated

@router.delete("/{task_id}")
async def delete_task_route(task_id: str):
    ok = delete_task(task_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"deleted": True}