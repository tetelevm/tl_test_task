from django.urls import path, re_path

from .views import main, get_children


__all__ = [
    "urlpatterns",
]


urlpatterns = [
    re_path(r"children(/(?P<department_id>\d+))?/$", get_children, name="children"),
    path("", main),
]
