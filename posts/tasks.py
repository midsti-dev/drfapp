from celery import shared_task
import time

import redis

from src import settings


@shared_task
def log_posts_opened():
    time.sleep(30)
    print("[CELERY TASK] Opened the posts")
    return "Opened the posts"


