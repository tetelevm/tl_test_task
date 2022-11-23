import json
import random
import datetime as dt
from pathlib import Path

from django.core.management import BaseCommand
from django.db.transaction import atomic
from django.contrib.auth.models import User

from ...models import DepartmentModel, PostModel, EmployeeModel


class Command(BaseCommand):
    help = (
        "It fills the database with data."
        " Creates superuser (admin/admin), department trees, posts, employees."
        " Apply only to an empty database!"
    )
    path_to_data = (Path(__file__).parent / "names").resolve()

    def _get_data_from_json(self, filename: str) -> dict:
        with open(self.path_to_data / filename) as json_file:
            data = json.load(json_file)
        return data

    def add_user(self):
        """
        Adds a superuser with login/password `admin/admin`
        (for django_admin).
        """

        user = User(
            username="admin",
            is_staff=True,
            is_superuser=True
        )
        user.set_password("admin")
        user.save()

    def add_departments(self):
        """
        Generates a department tree.
        Generation is based on data from the file with names for each
        level of the deportment. For each deportment of the current level
        all variants of the next level are generated
        (aaa, aab, ..., zzy, zzz).
        """

        level_attrs = self._get_data_from_json("departments.json")

        # empty value for generation of the first level
        tree = {"id": None, "parent_department_id": None, "children": []}

        parents = [tree]
        id_counter = 0
        for level in level_attrs.values():
            new_parents = []

            for parent in parents:
                for variant in level["variants"]:
                    id_counter += 1
                    departament = {
                        "id": id_counter,
                        "name": level["name"] + " of " + variant,
                        "parent_department_id": parent["id"],
                        "children": [],
                    }
                    parent["children"].append(departament)
                    new_parents.append(departament)

            parents = new_parents

        departments = DepartmentModel.objects.build_tree_nodes(tree)
        departments.pop(0)  # removing the first empty value
        DepartmentModel.objects.bulk_create(departments)

    def add_posts(self):
        """
        Creates a list of posts from a file.
        """

        post_names = self._get_data_from_json("posts.json")["names"]
        PostModel.objects.bulk_create(
            [
                PostModel(name=name)
                for name in post_names
            ]
        )

    def add_employees(self):
        """
        For each sector (lower level of department) creates users with
        each of the posts.
        The name, employment date and salary are randomly generated.
        """

        fios = self._get_data_from_json("employees.json")

        first_names, second_names, last_names = fios.values()
        today = dt.date.today()
        posts = PostModel.objects.all().values_list("id", flat=True)
        sectors = DepartmentModel.objects.filter(level=5).values_list("id", flat=True)

        get_name = lambda: (
            f"{random.choice(last_names)}"
            f" {random.choice(first_names)}"
            f" {random.choice(second_names)}"
        )
        get_date = lambda: today - dt.timedelta(days=random.randint(5, 1000))
        get_salary = lambda: random.randint(16, 512) * 1000

        EmployeeModel.objects.bulk_create(
            [
                EmployeeModel(
                    name=get_name(),
                    date_employment=get_date(),
                    post_id=post_id,
                    department_id=sector_id,
                    salary=get_salary(),
                    is_active=True,
                )
                for post_id in posts
                for sector_id in sectors
            ]
        )

    def handle(self, *args, **options):
        with atomic():
            print("Adding a superuser")
            self.add_user()

            print("Adding departments")
            self.add_departments()

            print("Adding posts")
            self.add_posts()

            print("Adding employees")
            self.add_employees()

        print("ok!")
