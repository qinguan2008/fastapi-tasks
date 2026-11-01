from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

# ==================== 内存数据源 ====================
tasks_db = [
    {"id": 1, "title": "玩儿原神", "completed": True},
    {"id": 2, "title": "玩儿崩铁", "completed": True},
    {"id": 3, "title": "玩儿鸣潮", "completed": False}
]

# 全局递增 ID
current_id = 3


# ==================== 请求体模型 ====================
# 新增模型
class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, description="任务标题，必填")
    completed: bool = False


# 修改模型（全部可选）
class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1)
    completed: Optional[bool] = None


# ==================== 接口实现 ====================

# 1. 新增任务 (POST)
@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task_in: TaskCreate):
    global current_id
    current_id += 1

    new_task = task_in.model_dump()
    new_task["id"] = current_id

    tasks_db.append(new_task)
    return new_task


# 2. 查询任务列表与筛选 (GET)
@app.get("/tasks")
def get_tasks(completed: bool = None):
    if completed is None:
        return tasks_db
    result = []
    for task in tasks_db:
        if task["completed"] == completed:
            result.append(task)
    return result


# 3. 查询单条任务 (GET)
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks_db:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")


# 4. 修改任务 (PATCH)
@app.patch("/tasks/{task_id}")
def update_task(task_id: int, task_in: TaskUpdate):
    for task in tasks_db:
        if task["id"] == task_id:
            update_data = task_in.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                task[key] = value
            return task
    raise HTTPException(status_code=404, detail="Task not found")


# 5. 删除任务 (DELETE)
@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    for index, task in enumerate(tasks_db):
        if task["id"] == task_id:
            tasks_db.pop(index)
            return  # 204 不返回内容

    raise HTTPException(status_code=404, detail="Task not found")


# 6. 健康检查 (GET)
@app.get("/health")
def get_health():
    return {"status": "ok", "message": "正常运行！"}