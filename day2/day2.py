from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI()

tasks_db = [
    {"id": 1, "title": "玩儿原神", "completed": True},
    {"id": 2, "title": "玩儿崩铁", "completed": True},
    {"id": 3, "title": "玩儿鸣潮", "completed": False}
]


# ==================== 第二天新增的内容开始 ====================

# 1. 定义请求体模型
class TaskCreate(BaseModel):
    # ... 表示必填，min_length=1 限制空字符串
    title: str = Field(..., min_length=1, description="任务标题，必填")
    completed: bool = False


# 2. 定义全局递增 ID（因为列表里最大是3，所以初始值设为3）
current_id = 3


# 3. 新增 POST 接口
@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task_in: TaskCreate):
    global current_id
    current_id += 1  # ID 递增

    # 将请求体转为字典，并加上生成的 id
    new_task = task_in.model_dump()
    new_task["id"] = current_id

    # 存入内存列表
    tasks_db.append(new_task)

    # 返回新任务
    return new_task


# ==================== 第二天新增的内容结束 ====================


# 下面是你的原有代码
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
