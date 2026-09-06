from typing import Literal

from celery.result import AsyncResult
from fastapi import FastAPI
from pydantic import BaseModel

from celery_app import celery
from tasks import (
    run_demo_command,
    train_ml_model,
    transform_data,
)


app = FastAPI(
    title="FastAPI + Celery + RabbitMQ Demo",
    version="1.0.0",
)


class TrainRequest(BaseModel):
    data: dict = {"sample": "data"}
    duration: int = 10


class TransformItem(BaseModel):
    value: int


class TransformRequest(BaseModel):
    data: list[TransformItem]


class CommandRequest(BaseModel):
    command: Literal[
        "date",
        "whoami",
        "python-version",
    ]


@app.get("/")
def root():
    return {
        "message": "FastAPI + Celery + RabbitMQ is running"
    }


@app.post("/train")
def start_ml_training(request: TrainRequest):

    task = train_ml_model.delay(
        request.data,
        request.duration,
    )

    return {
        "task_id": task.id,
        "status": "submitted",
    }


@app.post("/transform")
def start_data_transformation(request: TransformRequest):

    data = [
        item.model_dump()
        for item in request.data
    ]

    task = transform_data.delay(data)

    return {
        "task_id": task.id,
        "status": "submitted",
    }


@app.post("/execute")
def execute_command(request: CommandRequest):

    task = run_demo_command.delay(
        request.command
    )

    return {
        "task_id": task.id,
        "status": "submitted",
    }


@app.get("/tasks/{task_id}")
def get_task(task_id: str):

    task: AsyncResult = celery.AsyncResult(task_id)

    response = {
        "task_id": task_id,
        "status": task.status,
        "ready": task.ready(),
    }

    if task.status == "PROGRESS":
        response["progress"] = task.info

    elif task.successful():
        response["result"] = task.result

    elif task.failed():
        response["error"] = str(task.result)

    return response
