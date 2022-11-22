from django.contrib import admin
from django.forms import Textarea
from django.db.models.fields import TextField

from .models import Department, Post, Employee


class _FlatText(admin.ModelAdmin):
    formfield_overrides = {
        TextField: {"widget": Textarea(attrs={"rows": 1, "cols": 60})},
    }


@admin.register(Department)
class DepartmentAdmin(_FlatText):
    fields = (("name", "parent_department"),)


@admin.register(Post)
class PostAdmin(_FlatText):
    fields = ("name",)


@admin.register(Employee)
class QuestionChoiceAdmin(_FlatText):
    fields = (
        ("name",),
        ("date_employment", "is_active"),
        ("department", "post", "salary"),
    )


