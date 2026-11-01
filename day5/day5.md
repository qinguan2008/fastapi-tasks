# 第五天作业：路由组织与接口验证

## 一、 核心代码实现

本次作业利用 `APIRouter` 对代码进行了模块化拆分，以下是各个文件的完整代码。

### 1. 数据与模型 (database.py)
```python
tasks_db = [
    {"id": 1, "title": "玩儿原神", "completed": True},
    {"id": 2, "title": "玩儿崩铁", "completed": True},
    {"id": 3, "title": "玩儿鸣潮", "completed": False}
]

current_id = 3
```

### 2. 数据模型 (schemas.py)
```python
from pydantic import BaseModel, Field
from typing import Optional

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1)
    completed: bool = False

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1)
    completed: Optional[bool] = None
```

### 3. 路由文件 (routers/tasks.py)
```python
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
```

### 4. 主程序入口 (main.py)
```python
from fastapi import FastAPI
from routers import tasks

app = FastAPI()

app.include_router(tasks.router)

@app.get("/health")
def get_health():
    return {"status": "ok", "message": "正常运行！"}
```

## 二、 接口功能验证记录

### 1. 正常流程验证

**① 新增任务 (POST) 返回 201**
输入正常的 JSON 数据，服务端成功生成自增 ID。
![新增任务](1.png)
![新增任务](2.png)
![新增任务](3.png)

**② 查询与筛选 (GET) 返回 200**
测试 `completed=false` 的查询参数筛选，成功过滤出未完成的任务。
![查询筛选](4.png)
![查询筛选](5.png)

**③ 修改任务 (PATCH) 返回 200**
测试部分更新，仅修改 title，未传入的 completed 保持不变。
![修改任务](6.png)
![修改任务](7.png)
![修改任务](8.png)
![修改任务](9.png)
![修改任务](10.png)
![修改任务](11.png)

**④ 删除任务 (DELETE) 返回 204**
删除指定 ID 的任务，成功返回 204 且无响应体。
![删除任务](12.png)
![删除任务](13.png)

### 2. 异常输入验证

**① 查询不存在的 ID 返回 404**
请求 `GET /tasks/999`，服务端准确定位并返回 404 错误。
![404测试](14.png)
![404测试](15.png)

**② 非整数 ID 返回 422**
请求 `GET /tasks/abc`，触发 Pydantic 框架校验拦截，返回 422 错误。
![422测试](16.png)
![422测试](17.png)
![422测试](18.png)

## 三、 接口说明整理

| 请求方法 | 路径 | 请求体/参数 | 状态码 | 说明 |
| :--- | :--- | :--- | :--- | :--- |
| POST | /tasks | `{"title": "任务"}` | 201 | 创建任务 |
| GET | /tasks | `?completed=true` | 200 | 获取列表/筛选 |
| GET | /tasks/{id} | 路径参数 id | 200 / 404 | 获取单条任务 |
| PATCH | /tasks/{task_id} | `{"completed": true}` | 200 / 404 | 部分更新任务 |
| DELETE | /tasks/{task_id} | 路径参数 id | 204 / 404 | 删除任务 |