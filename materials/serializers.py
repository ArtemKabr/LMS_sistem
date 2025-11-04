from rest_framework import serializers
from .models import Course, Lesson
from users.models import User


class CourseSerializer(serializers.ModelSerializer):
    author_email = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ["id", "title", "description", "preview", "author", "author_email"]

    def get_author_email(self, obj):
        """Возвращает email автора, если он есть."""
        if obj.author:
            return obj.author.email
        return None


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "phone", "city", "avatar"]
