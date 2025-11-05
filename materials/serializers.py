from rest_framework import serializers
from users.models import User
from .models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):
    author_email = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ["id", "title", "description", "preview", "author", "author_email"]

    def get_author_email(self, obj):
        """Возвращает email автора, если он есть."""
        return obj.author.email if obj.author else None


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "phone", "city", "avatar"]
