from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import F, Value

from .models import DepartmentModel, EmployeeModel


__all__ = [
    "main",
    "get_children",
]


def main(request):
    """
    Returns the project's home page with or without a link to the admin
    panel, depending on the user's authorization.
    """

    is_authenticated = request.user and not request.user.is_anonymous
    return render(request, 'index.html', {"is_authenticated": is_authenticated})


def get_children(request, department_id=None):
    """
    The only api of the project, it returns the list of departments,
    that are subordinate to the given department, and the list of
    employees who work in the given department.
    """

    if isinstance(department_id, str):
        department_id = int(department_id)

    departments = DepartmentModel.objects.filter(
        parent_department_id=department_id
    ).values("id", "name", "parent_department_id", "level")

    employees = EmployeeModel.objects.filter(
        department_id=department_id
    ).annotate(
        post_name=F("post__name"),
        level=(
            F("department__level") + 1
            if department_id else
            Value(1)
        ),
    )
    employees = employees.values()

    child_objects = {
        "departments": list(departments),
        "employees": list(employees),
    }

    return JsonResponse(child_objects)
