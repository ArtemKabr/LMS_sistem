from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Payment

User = get_user_model()


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Payment"""
    class Meta:
        model = Payment
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели пользователя"""
    class Meta:
        model = User
        fields = ["id", "email", "phone", "city", "avatar"]


class UserProfileSerializer(serializers.ModelSerializer):
    """Сериализатор профиля пользователя с историей платежей"""
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ("id", "email", "payments")
