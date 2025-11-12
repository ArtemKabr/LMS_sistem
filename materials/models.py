# materials\models.py
from django.db import models
from users.models import User


class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="owned_courses",
        verbose_name="Владелец",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="authored_courses",
        verbose_name="Автор",
        null=True,
        blank=True,
    )
    preview = models.ImageField(upload_to="course_previews/", blank=True, null=True)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    preview = models.ImageField(
        upload_to="lesson_previews/", blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="owned_lessons",
        verbose_name="Владелец урока",
        null=False,
    )

    def __str__(self):
        return f"{self.title} ({self.course})"


class Subscription(models.Model):
    """Подписка пользователя на обновления курса"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="subscriptions",
        verbose_name="Пользователь",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="subscriptions",
        verbose_name="Курс",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата подписки",
    )

    class Meta:
        unique_together = ("user", "course")
        verbose_name = "Подписка на курс"
        verbose_name_plural = "Подписки на курсы"

    def __str__(self):
        return f"{self.user} → {self.course}"