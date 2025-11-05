from django.db import models
from users.models import User


class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    preview = models.ImageField(
        upload_to="course_previews/", blank=True, null=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="courses",
        verbose_name="Автор",
        null=True,
        blank=True,
    )

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

    def __str__(self):
        return f"{self.title} ({self.course})"
