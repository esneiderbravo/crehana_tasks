from fastapi import FastAPI
from src.api import users_router
from src.api.task_lists_router import router as task_lists_router
from src.api.tasks_router import router as tasks_router

app = FastAPI(title="Crehana Tasks API")

app.include_router(users_router.router)
app.include_router(task_lists_router)
app.include_router(tasks_router)


@app.get("/")
async def health_check():
    return {"status": "ok"}
