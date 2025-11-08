from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsModer, IsOwner
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """CRUD-контроллер для курсов с разграничением прав."""

    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Модераторы видят все курсы, пользователи — только свои."""
        user = self.request.user
        if user.groups.filter(name="moderators").exists():
            return Course.objects.all()
        return Course.objects.filter(owner=user)

    def perform_create(self, serializer):
        """Привязываем курс к текущему пользователю."""
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        """Определяем права в зависимости от действия."""
        if self.action in ["list", "retrieve"]:
            self.permission_classes = [IsAuthenticated]
        elif self.action in ["update", "partial_update"]:
            # редактировать может модератор или владелец
            self.permission_classes = [IsAuthenticated, IsModer | IsOwner]
        elif self.action in ["destroy", "create"]:
            # модераторы не могут создавать или удалять
            self.permission_classes = [IsAuthenticated, ~IsModer & IsOwner]
        else:
            self.permission_classes = [IsAuthenticated]
        return [perm() for perm in self.permission_classes]


class LessonViewSet(viewsets.ModelViewSet):
    """CRUD-контроллер для уроков с разграничением прав."""

    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Модераторы видят все уроки, пользователи — только свои."""
        user = self.request.user
        if user.groups.filter(name="moderators").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)

    def perform_create(self, serializer):
        """Привязываем урок к владельцу (создателю)."""
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            self.permission_classes = [IsAuthenticated]
        elif self.action in ["update", "partial_update"]:
            self.permission_classes = [IsAuthenticated, IsModer | IsOwner]
        elif self.action in ["destroy", "create"]:
            self.permission_classes = [IsAuthenticated, ~IsModer & IsOwner]
        else:
            self.permission_classes = [IsAuthenticated]
        return [perm() for perm in self.permission_classes]
