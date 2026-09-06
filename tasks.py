import os
from time import sleep

from celery import Celery


app = Celery(
    "tasks",
    broker=os.getenv(
        "CELERY_BROKER_URL",
        "amqp://celery:celery@rabbitmq:5672//",
    ),
    backend=os.getenv("CELERY_RESULT_BACKEND", "rpc://"),
)

app.conf.update(
    task_track_started=True,
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
)


@app.task
def process(x, y):
    i = 0
    while i < 5:
        sleep(1)
        i += 1
        print("Processing...")

    return x**2 + y**2
