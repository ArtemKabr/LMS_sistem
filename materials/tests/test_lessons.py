# materials/tests/test_lessons.py — тесты CRUD и валидации для уроков
from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from materials.models import Course, Lesson

User = get_user_model()


class LessonCrudTests(APITestCase):
    """Тесты CRUD для уроков + проверка валидатора ссылок."""

    def setUp(self):
        # Создаем пользователя и курс
        self.user = User.objects.create_user(email="user@example.com", password="pass12345")
        self.course = Course.objects.create(
            title="Python",
            description="Базовый курс",
            owner=self.user,
        )

        # Аутентифицируемся
        self.client.force_authenticate(user=self.user)
        self.list_url = reverse("lesson-list")

    def test_create_lesson_ok_with_youtube(self):
        """Создание урока с корректной YouTube-ссылкой должно пройти успешно."""
        payload = {
            "title": "Урок 1",
            "description": "Введение",
            "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "course": self.course.id,
        }
        resp = self.client.post(self.list_url, data=payload, format="json")
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(Lesson.objects.count(), 1)

    def test_create_lesson_reject_non_youtube(self):
        """Создание урока с не-YouTube ссылкой должно возвращать 400."""
        payload = {
            "title": "Урок 2",
            "description": "Сторонняя ссылка",
            "video_url": "https://vimeo.com/123",
            "course": self.course.id,
        }
        resp = self.client.post(self.list_url, data=payload, format="json")
        self.assertEqual(resp.status_code, 400)
        self.assertIn("youtube", str(resp.data).lower())

    def test_list_lessons_paginated(self):
        """Проверка пагинации списка уроков (по умолчанию 10 на страницу)."""
        Lesson.objects.bulk_create([
            Lesson(title=f"Урок {i}", description="", course=self.course, owner=self.user)
            for i in range(1, 16)
        ])
        resp = self.client.get(self.list_url)
        self.assertEqual(resp.status_code, 200)
        # DRF PageNumberPagination по умолчанию возвращает count, next, previous, results
        self.assertIn("results", resp.data)
        self.assertLessEqual(len(resp.data["results"]), 10)
