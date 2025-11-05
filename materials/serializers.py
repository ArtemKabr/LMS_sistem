from rest_framework import serializers
from users.models import User
from .models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для модели урока"""
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
        ]

    def get_author_email(self, obj):
        """Возвращает email автора, если он есть."""
        return obj.author.email if obj.author else None

    def get_lessons_count(self, obj):
        """Подсчитывает количество уроков в курсе"""
        return obj.lessons.count()


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
