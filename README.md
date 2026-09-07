# FastAPI, Celery and RabbitMQ

Un exemple simple pour exécuter une tâche Celery depuis une API FastAPI.
- **RabbitMQ** est le broker : il transporte et garde les messages en attente.
- **Celery** gère les tâches et les workers qui les exécutent.
- **FastAPI** reçoit les requêtes HTTP et délègue les traitements.

## Start

```bash
docker compose up --build
```

- API : <http://localhost:8000/docs>
- Interface : <http://localhost:8000>
- RabbitMQ : <http://localhost:15672>
- RabbitMQ login : `celery` / `celery`

## Example

Soumettre une tâche :

```bash
curl -X POST http://localhost:8000/tasks \
  -H 'Content-Type: application/json' \
  -d '{"x": 3, "y": 4}'
```

Consulter le résultat avec le `task_id` reçu :

```bash
curl http://localhost:8000/tasks/{task-id}
```

La tâche calcule `x² + y²`. Le résultat de `3² + 4²` est `25`.
