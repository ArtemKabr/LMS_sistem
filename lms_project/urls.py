from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path

urlpatterns = [
    path("", lambda request: HttpResponse("<h2>Добро пожаловать в LMS API 🚀</h2>")), ### ВНИМАНИЕ КАК ПОЯВИТСЯ ФРОНТ ЭТО УБРАТЬ
    path("admin/", admin.site.urls),
    path("api/", include("materials.urls")),
    path("users/", include("users.urls")),
]
