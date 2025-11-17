# users/serializers.py — сериализаторы пользователей

from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Полный сериализатор для пользователя."""
    class Meta:
        model = User
        fields = ["id", "email", "phone", "city", "avatar"]


class UserProfileSerializer(serializers.ModelSerializer):
    """Сериализатор профиля пользователя (без платежей)."""

    class Meta:
        model = User
        fields = ["id", "email", "phone", "city", "avatar"]


class PublicUserSerializer(serializers.ModelSerializer):
    """Публичный сериализатор (для просмотра чужих профилей)."""
    class Meta:
        model = User
        fields = ["id", "email", "city", "avatar"]


class RegisterSerializer(serializers.ModelSerializer):
    """Сериализатор регистрации нового пользователя."""
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "password"]

    def create(self, validated_data):
        return User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
        )