from django.urls import include, path

from .views import UserProfileUpdateView

urlpatterns = [
    path("profile/<int:pk>/", UserProfileUpdateView.as_view(), name="user-profile"),
    path("api/users/", include("users.urls")),
]
