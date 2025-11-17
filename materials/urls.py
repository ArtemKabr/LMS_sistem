# materials/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CourseViewSet, LessonViewSet, PaymentCreateAPIView
from .views_subscriptions import SubscriptionToggleAPIView


router = DefaultRouter()
router.register(r"courses", CourseViewSet, basename="course")
router.register(r"lessons", LessonViewSet, basename="lesson")

urlpatterns = [
    path("", include(router.urls)),
    path("subscriptions/toggle/", SubscriptionToggleAPIView.as_view(), name="subscription-toggle"),
    path("payments/create/", PaymentCreateAPIView.as_view(), name="payment-create"),
]
