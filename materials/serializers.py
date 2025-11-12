from rest_framework import serializers
from .models import Course, Lesson, Subscription
from .validators import validate_youtube_url
from .models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для модели урока"""

    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    video_url = serializers.CharField(
        required=False,
        allow_blank=True,
        validators=[validate_youtube_url],
    )

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели курса.
    Добавлены:
    - email автора (author_email)
    - количество уроков (lessons_count)
    - список уроков (lessons)
    """
    author_email = serializers.SerializerMethodField()
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, source="lesson_set", read_only=True)
    is_subscribed = serializers.SerializerMethodField(
        help_text="Пользователь подписан?"
    )

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "description",
            "preview",
            "author",
            "author_email",
            "lessons_count",
            "lessons",
            "is_subscribed",
        ]

    def get_author_email(self, obj):
        """Возвращает email автора, если он есть."""
        return obj.author.email if obj.author else None

    def get_lessons_count(self, obj):
        """Подсчитывает количество уроков в курсе"""
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        """Проверяет, подписан ли текущий пользователь на курс"""
        request = self.context.get("request")
        user = getattr(request, "user", None)
        if not user or not user.is_authenticated:
            return False
        return Subscription.objects.filter(user=user, course=obj).exists()


class CourseDetailSerializer(serializers.ModelSerializer):
    """Сериализатор курса с уроками и количеством"""
    lessons = LessonSerializer(many=True, source="lesson_set", read_only=True)
    lessons_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ("id", "title", "description", "lessons_count", "lessons")

    def get_lessons_count(self, obj):
        """Возвращает количество уроков в курсе"""
        return obj.lessons.count()
