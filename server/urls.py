from django.contrib import admin
from django.urls import path, include


__all__ = [
    "urlpatterns",
]


urlpatterns = [
    path("", include("employees.urls")),
    path("admin/", admin.site.urls),
]
