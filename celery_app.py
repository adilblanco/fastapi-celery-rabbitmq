import os

from celery import Celery


broker_url = os.getenv(
    "CELERY_BROKER_URL",
    "amqp://celery:celery@rabbitmq:5672//",
)

result_backend = os.getenv(
    "CELERY_RESULT_BACKEND",
    "rpc://",
)


celery = Celery(
    "worker",
    broker=broker_url,
    backend=result_backend,
    include=["tasks"],
)


celery.conf.update(
    task_track_started=True,
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
)
