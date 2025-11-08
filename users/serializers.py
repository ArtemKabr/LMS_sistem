from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Payment

User = get_user_model()


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Payment."""
    class Meta:
        model = Payment
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    """Полный сериализатор для пользователя."""
    class Meta:
        model = User
        fields = ["id", "email", "phone", "city", "avatar"]


class UserProfileSerializer(serializers.ModelSerializer):
    """Сериализатор профиля пользователя с историей платежей."""
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ("id", "email", "payments")


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
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user
