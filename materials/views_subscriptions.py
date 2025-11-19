# materials/views_subscriptions.py
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Course, Subscription

class SubscriptionToggleAPIView(APIView):
    """
    POST: переключает подписку текущего пользователя на курс.
    Вход: {"course_id": <int>}
    Выход: {"message": "подписка добавлена|подписка удалена"}
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get("course_id")
        course = get_object_or_404(Course, pk=course_id)

        qs = Subscription.objects.filter(user=user, course=course)
        if qs.exists():
            qs.delete()
            message = "подписка удалена"
        else:
            Subscription.objects.create(user=user, course=course)
            message = "подписка добавлена"

        return Response({"message": message})
