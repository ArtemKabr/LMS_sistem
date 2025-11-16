# materials/serializers.py — сериализаторы курсов, уроков и платежей
from rest_framework import serializers
from .models import Course, Lesson, Subscription, Payment
from .validators import validate_youtube_url


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор урока"""

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
    """Сериализатор курса"""

    author_email = serializers.SerializerMethodField()
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

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
        return obj.author.email if obj.author else None

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        request = self.context.get("request")
        user = getattr(request, "user", None)
        if not user or not user.is_authenticated:
            return False
        return Subscription.objects.filter(user=user, course=obj).exists()


class CourseDetailSerializer(serializers.ModelSerializer):
    """Детальный сериализатор курса"""

    lessons = LessonSerializer(many=True, read_only=True)
    lessons_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ("id", "title", "description", "lessons_count", "lessons")

    def get_lessons_count(self, obj):
        return obj.lessons.count()


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализатор платежа"""

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = (
            "stripe_product_id",
            "stripe_price_id",
            "stripe_session_id",
            "payment_url",
        )
