# users/views.py

from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import User, Payment
from .serializers import UserSerializer, PaymentSerializer


class UserProfileUpdateView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PaymentListView(generics.ListAPIView):
    """Эндпоинт для фильтрации и сортировки платежей"""
    queryset = Payment.objects.all().order_by("-date")
    serializer_class = PaymentSerializer

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["paid_course", "paid_lesson", "method"]
    ordering_fields = ["date"]
