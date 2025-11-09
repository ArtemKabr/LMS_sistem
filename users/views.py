from rest_framework import generics, filters, viewsets
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Payment
from .serializers import (
    UserSerializer,
    PaymentSerializer,
    RegisterSerializer,
    UserProfileSerializer,
    PublicUserSerializer,
)

User = get_user_model()


class UserProfileUpdateView(generics.RetrieveUpdateAPIView):
    """
    Эндпоинт для просмотра и редактирования профиля пользователя.
    Авторизованный пользователь может редактировать только свой профиль.
    При просмотре чужого профиля — видит только ограниченные поля.
    """

    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """Определяем, какой сериализатор использовать."""
        # если пользователь просматривает себя — показываем полный профиль
        if self.request.user.pk == self.kwargs.get("pk"):
            return UserProfileSerializer
        # если чужой профиль — только публичные поля
        return PublicUserSerializer


class PaymentListView(generics.ListAPIView):
    """
    Эндпоинт для получения списка платежей с фильтрацией и сортировкой.
    """
    queryset = Payment.objects.all().order_by("-date")
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["paid_course", "paid_lesson", "method"]
    ordering_fields = ["date"]


class RegisterAPIView(generics.CreateAPIView):
    """
    Эндпоинт для регистрации новых пользователей.
    Доступен без авторизации.
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class UserViewSet(viewsets.ModelViewSet):
    """
    CRUD для пользователей.
    Доступен только авторизованным пользователям.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
