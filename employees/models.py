from django.db.models import Model, Index, Q, PROTECT
from django.db.models import ForeignKey, TextField, DateField, BooleanField, IntegerField
from django.core.validators import MinValueValidator
from django.db.models.constraints import CheckConstraint
from mptt.models import MPTTModel, TreeForeignKey


__all__ = [
    "Department",
    "Post",
    "Employee",
]


_max_nesting_level = 5


class Department(MPTTModel):
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


class Post(Model):
    name = TextField(
        verbose_name="Post name",
        null=False,
        unique=True,
    )

    def __str__(self):
        return self.name


class Employee(Model):
    name = TextField(
        verbose_name="Full name",
        null=False,
    )
    date_employment = DateField(
        verbose_name="Date of employment",
        null=False,
    )
    post = ForeignKey(
        "employees.Post",
        verbose_name="Employee post",
        on_delete=PROTECT
    )
    department = ForeignKey(
        "employees.Department",
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
    is_active = BooleanField(
        verbose_name="Is employee working",
        default=True,
    )

    class Meta:
        indexes = [
            Index(fields=["date_employment"]),
            Index(fields=["is_active"]),
        ]
        constraints = [
            CheckConstraint(
                check=(
                    (Q(is_active=True) & Q(department_id__isnull=False))
                    | (Q(is_active=False) & Q(department_id__isnull=True))
                ),
                name="works_in_department"
            ),
        ]

