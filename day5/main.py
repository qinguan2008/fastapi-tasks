from fastapi import FastAPI
from routers import tasks

app = FastAPI()

app.include_router(tasks.router)

@app.get("/health")
def get_health():
    return {"status": "ok", "message": "正常运行！"}
