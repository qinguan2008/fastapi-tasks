from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from fastapi.openapi.docs import get_swagger_ui_html

app = FastAPI(docs_url=None)

tasks_db = [
    {"id": 1, "title": "玩儿原神", "completed": True},
    {"id": 2, "title": "玩儿崩铁", "completed": True},
    {"id": 3, "title": "玩儿鸣潮", "completed": False}
]

# 第二天：POST新增
class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, description="任务标题，必填")
    completed: bool = False

current_id = 3

@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task_in: TaskCreate):
    global current_id
    current_id += 1
    new_task = task_in.model_dump()
    new_task["id"] = current_id
    tasks_db.append(new_task)
    return new_task

# 原有GET接口
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
    return result

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks_db:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

# 国内CDN，解决docs白屏
@app.get("/docs", include_in_schema=False)
async def custom_docs():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="Task API",
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css"
    )

