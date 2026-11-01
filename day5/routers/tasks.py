from fastapi import APIRouter, HTTPException, status
from schemas import TaskCreate, TaskUpdate
import database

router = APIRouter()

@router.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task_in: TaskCreate):
    database.current_id += 1
    new_task = task_in.model_dump()
    new_task["id"] = database.current_id
    database.tasks_db.append(new_task)
    return new_task

@router.get("/tasks")
def get_tasks(completed: bool = None):
    if completed is None:
        return database.tasks_db
    return [t for t in database.tasks_db if t["completed"] == completed]

@router.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in database.tasks_db:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@router.patch("/tasks/{task_id}")
def update_task(task_id: int, task_in: TaskUpdate):
    for task in database.tasks_db:
        if task["id"] == task_id:
            update_data = task_in.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                task[key] = value
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@router.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    for index, task in enumerate(database.tasks_db):
        if task["id"] == task_id:
            database.tasks_db.pop(index)
            return
    raise HTTPException(status_code=404, detail="Task not found")