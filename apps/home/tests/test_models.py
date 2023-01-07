from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.home.models import Employee


class ModelsTests(TestCase):

    def test_employee_str(self):

        employee = get_user_model().objects.create_user(
            username="test",
            password="test12345",
            first_name="test first",
            last_name="Test last"
        )

        self.assertEqual(
            str(employee),
            f"{employee.username} "
            f"({employee.first_name} "
            f"{employee.last_name})")
