from datetime import datetime

from celery import shared_task

from users.models import User


@shared_task
def check_last_login():
    users = User.objects.filter(is_superuser=False)
    for user in users:
        today = datetime.today().date()
        if (today - user.last_login).days > 90:
            user.is_active = False
            user.save()
        print(f"{user.id} is now not active")


