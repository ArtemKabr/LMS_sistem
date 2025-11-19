# users/views.py — вьюхи приложения пользователей

from rest_framework import generics, viewsets
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import (
    UserProfileSerializer,
    PublicUserSerializer,
    RegisterSerializer,
    UserSerializer,
)

User = get_user_model()


class UserProfileUpdateView(generics.RetrieveUpdateAPIView):
    """
    Эндпоинт для просмотра и редактирования профиля пользователя.
    """

    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """Определяем, какой сериализатор использовать."""
        if self.request.user.pk == self.kwargs.get("pk"):
            return UserProfileSerializer
        return PublicUserSerializer


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