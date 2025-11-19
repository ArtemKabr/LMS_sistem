# materials/tests/test_subscriptions.py — тесты для функционала подписок
from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from materials.models import Course, Subscription

User = get_user_model()


class SubscriptionToggleTests(APITestCase):
    """Тестируем установку/удаление подписки и признак is_subscribed."""

    def setUp(self):
        self.user = User.objects.create_user(email="user@example.com", password="pass12345")
        self.course = Course.objects.create(
            title="Django",
            description="DRF",
            owner=self.user,
        )
        self.client.force_authenticate(self.user)
        self.toggle_url = reverse("subscription-toggle")
        self.course_detail_url = reverse("course-detail", args=[self.course.id])

    def test_toggle_subscription_add_and_remove(self):
        """Тест добавления и удаления подписки."""
        # Добавить подписку
        resp_add = self.client.post(self.toggle_url, data={"course_id": self.course.id}, format="json")
        self.assertEqual(resp_add.status_code, 200)
        self.assertEqual(resp_add.data["message"], "подписка добавлена")
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

        # Удалить подписку
        resp_del = self.client.post(self.toggle_url, data={"course_id": self.course.id}, format="json")
        self.assertEqual(resp_del.status_code, 200)
        self.assertEqual(resp_del.data["message"], "подписка удалена")
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_course_detail_contains_is_subscribed_flag(self):
        """Тест флага is_subscribed в деталях курса."""
        # По умолчанию не подписан
        resp1 = self.client.get(self.course_detail_url)
        self.assertEqual(resp1.status_code, 200)
        self.assertIn("is_subscribed", resp1.data)
        self.assertFalse(resp1.data["is_subscribed"])

        # Подписаться
        self.client.post(self.toggle_url, data={"course_id": self.course.id}, format="json")

        # Теперь признак True
        resp2 = self.client.get(self.course_detail_url)
        self.assertTrue(resp2.data["is_subscribed"])
