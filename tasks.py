import subprocess
import sys
import time

from celery_app import celery


@celery.task(bind=True)
def train_ml_model(self, data: dict, duration: int = 10):
    """
    Simulation d'un entraînement ML qui prend plusieurs secondes.
    """

    for i in range(duration):
        time.sleep(1)

        self.update_state(
            state="PROGRESS",
            meta={
                "current": i + 1,
                "total": duration,
            },
        )

    return {
        "status": "ML model trained",
        "input": data,
    }


@celery.task
def transform_data(data: list[dict]):
    """
    Double la valeur de chaque élément.
    """

    time.sleep(5)

    transformed = [
        {
            **item,
            "value": item["value"] * 2,
        }
        for item in data
    ]

    return transformed


@celery.task
def run_demo_command(command: str):
    """
    Exécute seulement quelques commandes autorisées.
    """

    allowed_commands = {
        "date": ["date"],
        "whoami": ["whoami"],
        "python-version": [sys.executable, "--version"],
    }

    if command not in allowed_commands:
        raise ValueError(
            f"Command not allowed: {command}"
        )

    result = subprocess.run(
        allowed_commands[command],
        capture_output=True,
        text=True,
        check=True,
    )

    return result.stdout.strip() or result.stderr.strip()
