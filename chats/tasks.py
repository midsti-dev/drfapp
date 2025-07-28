# chats/tasks.py

from celery import shared_task
import redis
from django.conf import settings


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

