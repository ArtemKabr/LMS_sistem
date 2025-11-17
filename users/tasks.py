# users/tasks.py — периодические задачи пользователей

from datetime import timedelta
from django.utils import timezone

from celery import shared_task
from users.models import User


@shared_task
def deactivate_inactive_users():
    """
    Деактивирует пользователей, которые не заходили более 30 дней.
    """
    cutoff = timezone.now() - timedelta(days=30)

    inactive_users = User.objects.filter(
        is_active=True,
        last_login__lt=cutoff
    )

    count = inactive_users.count()
    inactive_users.update(is_active=False)

    return f"Deactivated users: {count}"
