from django.db.models import Model, Index, Q, PROTECT
from django.db.models import ForeignKey, TextField, DateField, BooleanField, IntegerField
from django.core.validators import MinValueValidator
from django.db.models.constraints import CheckConstraint
from mptt.models import MPTTModel, TreeForeignKey


__all__ = [
    "DepartmentModel",
    "PostModel",
    "EmployeeModel",
]


_max_nesting_level = 5


class DepartmentModel(MPTTModel):
    """
    Department model. A department has a name and may belong to a higher
    level department. The maximum level of nesting of departments is 5.
    """

    MAX_NESTING_LEVEL = _max_nesting_level

    name = TextField(
        verbose_name="Department name",
        null=False,
    )
    parent_department = TreeForeignKey(
        "self",
        verbose_name="Parent department",
        on_delete=PROTECT,
        null=True,
        blank=True,
    )

    class Meta:
        constraints = [
            CheckConstraint(
                check=Q(level__lte=_max_nesting_level),
                name="not_very_nest"
            ),
        ]

    class MPTTMeta:
        order_insertion_by = ["-id"]
        parent_attr = "parent_department"

    def __str__(self):
        return self.name


class PostModel(Model):
    """
    Model post, it contains only the title of the post.
    """

    name = TextField(
        verbose_name="Post name",
        null=False,
        unique=True,
    )

    def __str__(self):
        return self.name


class EmployeeModel(Model):
    """
    An employee model that contains all the required fields.
    """

    name = TextField(
        verbose_name="Full name",
        null=False,
    )
    date_employment = DateField(
        verbose_name="Date of employment",
        null=False,
    )
    post = ForeignKey(
        "employees.PostModel",
        verbose_name="Employee post",
        on_delete=PROTECT
    )
    department = ForeignKey(
        "employees.DepartmentModel",
        verbose_name="Department",
        on_delete=PROTECT,
        null=True,
        blank=True,
    )
    salary = IntegerField(
        verbose_name="Employee salary",
        null=False,
        default=0,
        validators=[MinValueValidator(0)],
    )

    class Meta:
        indexes = [
            Index(fields=["date_employment"]),
        ]

    def __str__(self):
        return self.name
