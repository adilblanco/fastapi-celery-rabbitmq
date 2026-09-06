from celery.result import AsyncResult
from fastapi import FastAPI
from pydantic import BaseModel

from tasks import app as celery_app
from tasks import process


app = FastAPI(title="Découvrir FastAPI, Celery et RabbitMQ")


class ProcessRequest(BaseModel):
    x: int
    y: int


@app.post("/tasks", status_code=202)
def submit_task(request: ProcessRequest):
    """Place une tâche dans RabbitMQ sans attendre son exécution."""
    task = process.delay(request.x, request.y)

    return {
        "task_id": task.id,
        "status": "submitted",
    }


@app.get("/tasks/{task_id}")
def read_task(task_id: str):
    """Consulte l'état et, lorsqu'il est disponible, le résultat."""
    task: AsyncResult = celery_app.AsyncResult(task_id)

    response = {
        "task_id": task_id,
        "status": task.status,
        "ready": task.ready(),
    }

    if task.successful():
        response["result"] = task.result
    elif task.failed():
        response["error"] = str(task.result)

    return response
