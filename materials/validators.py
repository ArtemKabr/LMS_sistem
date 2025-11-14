# materials/validators.py
from urllib.parse import urlparse
from rest_framework import serializers

ALLOWED_YT_HOSTS = {
    "youtube.com", "www.youtube.com", "m.youtube.com", "youtu.be"
}

def validate_youtube_url(value: str) -> str:
    """
    Валидатор ссылок на видео: разрешены только домены YouTube.
    Пустые значения пропускаем (если поле не обязательное).
    """
    if not value:
        return value

    parsed = urlparse(value)
    host = (parsed.netloc or "").lower()

    if host not in ALLOWED_YT_HOSTS:
        raise serializers.ValidationError(
            "Разрешены только ссылки на YouTube (youtube.com / youtu.be)."
        )
    return value


class YoutubeOnlyValidator:
    """
    Класс-валидатор для использования через Meta.validators сериализатора.
    Проверяет конкретное поле (например, 'video_url').
    """
    def __init__(self, field: str):
        self.field = field

    def __call__(self, attrs):
        value = attrs.get(self.field)
        validate_youtube_url(value)
        return attrs
