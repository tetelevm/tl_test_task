from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from django.shortcuts import redirect


__all__ = [
    "urlpatterns",
]


def favicon(request):
    return redirect('/static/img/logo.ico')


urlpatterns = [
    path("", include("employees.urls")),
    path("admin/", admin.site.urls),
    path('favicon.ico', favicon),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
