from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional  # 第三天新增：导入 Optional

app = FastAPI()

# 内存数据源
tasks_db = [
    {"id": 1, "title": "玩儿原神", "completed": True},
    {"id": 2, "title": "玩儿崩铁", "completed": True},
    {"id": 3, "title": "玩儿鸣潮", "completed": False}
]

# 全局递增 ID
current_id = 3


# ==================== 第二天：新增 (POST) ====================
class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, description="任务标题，必填")
    completed: bool = False


@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task_in: TaskCreate):
    global current_id
    current_id += 1

    new_task = task_in.model_dump()
    new_task["id"] = current_id

    tasks_db.append(new_task)
    return new_task


# ==================== 第三天：修改 (PATCH) ====================
# 1. 独立修改请求模型（所有字段设为可选）
class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1)
    completed: Optional[bool] = None


# 2. 实现 PATCH 接口
@app.patch("/tasks/{task_id}")
def update_task(task_id: int, task_in: TaskUpdate):
    for task in tasks_db:
        if task["id"] == task_id:
            # 核心魔法：只提取实际传入的字段
            update_data = task_in.model_dump(exclude_unset=True)

            # 遍历更新未传字段保持不变
            for key, value in update_data.items():
                task[key] = value

            return task

    raise HTTPException(status_code=404, detail="Task not found")


# ==================== 原有接口 (GET) ====================
@app.get("/health")
def get_health():
    return {"status": "ok", "message": "正常运行！"}


@app.get("/tasks")
def get_tasks(completed: bool = None):
    if completed is None:
        return tasks_db
    result = []
    for task in tasks_db:
        if task["completed"] == completed:
            result.append(task)
    if len(result) == 0:
        return []
    return result


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks_db:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")