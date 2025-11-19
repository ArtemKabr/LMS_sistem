# materials/tasks.py — Celery-задачи для уведомлений
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta

from celery import shared_task

from materials.models import Course, Subscription


@shared_task
def send_course_update_email(course_id: int):
    """Асинхронная отправка писем подписчикам курса"""
    course = Course.objects.get(id=course_id)
    subs = Subscription.objects.filter(course=course)

    emails = [sub.user.email for sub in subs if sub.user.email]

    if emails:
        send_mail(
            subject=f"Обновление курса: {course.title}",
            message="Материалы курса были обновлены.",
            from_email="noreply@example.com",
            recipient_list=emails,
            fail_silently=True,
        )


@shared_task
def send_course_update_if_old(course_id: int):
    """Отправка уведомления только если обновление было > 4 часов назад"""
    course = Course.objects.get(id=course_id)

    if not course.updated_at:
        return

    if timezone.now() - course.updated_at >= timedelta(hours=4):
        send_course_update_email.delay(course_id)
