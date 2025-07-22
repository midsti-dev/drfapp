from celery import shared_task
import time

import redis

from src import settings


@shared_task
def test_celery_task(message: str) -> str:
    time.sleep(3)  # симулируем работу
    print(f"[CELERY TASK] Получено сообщение: {message}")
    return f"Сообщение обработано: {message}"


@shared_task
def log_posts_opened():
    time.sleep(30)
    print("[CELERY TASK] Opened the posts")
    return "Opened the posts"


@shared_task
def check_active_users():
    r = redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
        decode_responses=True,
    )
    users = r.smembers("active_users")
    print(f"[Celery] Active WebSocket users: {users}")