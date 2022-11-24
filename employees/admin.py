from django.contrib import admin
from django.forms import Textarea
from django.db.models.fields import TextField

from .models import DepartmentModel, PostModel, EmployeeModel


class _FlatText(admin.ModelAdmin):
    formfield_overrides = {
        TextField: {"widget": Textarea(attrs={"rows": 1, "cols": 60})},
    }


@admin.register(DepartmentModel)
class DepartmentAdmin(_FlatText):
    fields = (("name", "parent_department"),)


@admin.register(PostModel)
class PostAdmin(_FlatText):
    fields = ("name",)


@admin.register(EmployeeModel)
class QuestionChoiceAdmin(_FlatText):
    fields = (
        ("name", "date_employment"),
        ("department", "post", "salary"),
    )
