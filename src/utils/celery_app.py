from celery import Celery

celery_app = Celery(
    "analisador",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

celery_app.conf.task_routes = {"src.tasks.*": {"queue": "analisador"}}