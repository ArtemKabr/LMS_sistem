# lms_project/urls.py — маршруты проекта и документации

from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,            # я добавил #
    SpectacularSwaggerView,        # я добавил #
    SpectacularRedocView,          # я добавил #
)

urlpatterns = [
    path(
        "",
        lambda request: HttpResponse("<h2>Добро пожаловать в LMS API 🚀</h2>")
    ),  # ⚠️ убрать когда появится фронт

    path("admin/", admin.site.urls),

    # Основные приложения
    path("api/", include("materials.urls")),
    path("users/", include("users.urls")),

    # Документация OpenAPI
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),  # JSON #
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]
