from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели пользователя.
    Позволяет получать и обновлять профиль пользователя через API.
    """
    class Meta:
        model = User
        # Можно ограничить поля, если не хочешь всё отдавать
        fields = ["id", "username", "email", "first_name", "last_name"]
        read_only_fields = ["id", "username"]
