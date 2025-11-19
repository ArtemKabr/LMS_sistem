# materials/views.py — вьюхи курсов, уроков и платежей

from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, AllowAny

from users.permissions import IsModer, IsOwner
from .models import Course, Lesson, Payment
from .serializers import CourseSerializer, LessonSerializer, PaymentSerializer
from .paginators import DefaultPagination
from .services.stripe_service import (
    create_stripe_product,
    create_stripe_price,
    create_checkout_session,
)

# Celery-задачи (я добавил)
from materials.tasks import send_course_update_email, send_course_update_if_old


class CourseViewSet(viewsets.ModelViewSet):
    """CRUD-контроллер курсов с корректным распределением прав."""

    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = DefaultPagination

    def get_queryset(self):
        """Модераторам показываем все курсы, пользователю — только свои."""
        user = self.request.user
        if user.groups.filter(name="moderators").exists():
            return Course.objects.all()
        return Course.objects.filter(owner=user)

    def perform_create(self, serializer):
        """Связываем курс с пользователем."""
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):  # (я добавил)
        """
        При обновлении курса отправляем уведомления подписчикам:
        1) обычная рассылка
        2) доп. задание — отправка только если курс не обновлялся > 4 часов
        """
        course = serializer.save()

        # Асинхронная отправка уведомления подписчикам (я добавил)
        send_course_update_email.delay(course.id)

        # Условная отправка при старом обновлении (я добавил)
        send_course_update_if_old.delay(course.id)

    def get_permissions(self):
        """Задаём права на действия."""
        if self.action in ["list", "retrieve"]:
            return [IsAuthenticated()]
        if self.action in ["update", "partial_update"]:
            return [IsAuthenticated(), IsModer() or IsOwner()]
        if self.action in ["create", "destroy"]:
            return [IsAuthenticated(), IsOwner()]
        return [IsAuthenticated()]


class LessonViewSet(viewsets.ModelViewSet):
    """CRUD-контроллер уроков."""

    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = DefaultPagination

    def get_queryset(self):
        """Модераторы видят все уроки, пользователи — только свои."""
        user = self.request.user
        if user.groups.filter(name="moderators").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)

    def perform_create(self, serializer):
        """Привязываем урок к автору."""
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):  # (я добавил)
        """
        При обновлении урока выполняем доп. условие:
        отправлять уведомление только если курс не обновлялся > 4 часов.
        """
        lesson = serializer.save()
        course_id = lesson.course.id

        # Отправка по доп. условию (я добавил)
        send_course_update_if_old.delay(course_id)

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [IsAuthenticated()]
        if self.action in ["update", "partial_update"]:
            return [IsAuthenticated(), IsModer() or IsOwner()]
        if self.action in ["create", "destroy"]:
            return [IsAuthenticated(), IsOwner()]
        return [IsAuthenticated()]


class PaymentCreateAPIView(generics.CreateAPIView):
    """Создание Stripe-платежа."""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        """
        Создаём локальный объект + продукт Stripe + цену + сессию.
        """
        payment = serializer.save()

        stripe_product_id = create_stripe_product(payment.course)
        stripe_price_id = create_stripe_price(stripe_product_id, payment.amount)
        session_data = create_checkout_session(stripe_price_id)

        payment.stripe_product_id = stripe_product_id
        payment.stripe_price_id = stripe_price_id
        payment.stripe_session_id = session_data["id"]
        payment.payment_url = session_data["url"]
        payment.save()
