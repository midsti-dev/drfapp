from datetime import datetime, timedelta
from celery import shared_task
from django.db import transaction
from django.utils.timezone import make_aware
from users.models import User


@shared_task
def check_last_login():
    cutoff = make_aware(datetime.now() - timedelta(days=90))

    queryset = User.objects.filter(is_superuser=False, last_login__lt=cutoff).only('id', 'is_active', 'last_login')

    batch_size = 500
    batch = []

    for user in queryset.iterator():
        user.is_active = False
        batch.append(user)

        if len(batch) == batch_size:
            _bulk_save(batch)
            print(f"Processed batch of {batch_size} users")
            batch = []

    if batch:
        _bulk_save(batch)
        print(f"Processed final batch of {len(batch)} users")


def _bulk_save(users):
    # Сохраняем всех пользователей одной транзакцией
    with transaction.atomic():
        User.objects.bulk_update(users, ['is_active'])



