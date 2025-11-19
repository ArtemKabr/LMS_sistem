# materials/models.py — модели курсов, уроков, подписок и платежей  # (я добавил)
from django.db import models
from users.models import User
from django.conf import settings


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
        Course,
        on_delete=models.CASCADE,
        related_name="lessons",
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    preview = models.ImageField(
        upload_to="lesson_previews/",
        blank=True,
        null=True,
    )
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


class Payment(models.Model):
    """Платёж пользователя за курс"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="material_payments",
        verbose_name="Пользователь",
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="payments",
        verbose_name="Курс",
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Сумма оплаты",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
    )

    # === поля Stripe ===
    stripe_product_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="ID продукта Stripe",
    )

    stripe_price_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="ID цены Stripe",
    )

    stripe_session_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="ID сессии Stripe",
    )

    payment_url = models.CharField(
        max_length=1000,
        blank=True,
        null=True,
        verbose_name="Ссылка на оплату Stripe",
    )

    def __str__(self):
        return f"Платёж {self.id} пользователя {self.user}"
