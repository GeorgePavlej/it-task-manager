from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.home.forms import EmployeeSearchForm
from apps.home.models import Employee, Position


class EmployeeSearchTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_user",
        )
        self.client.force_login(self.user)

    def test_search_employee_by_username(self):
        response = self.client.get(
            reverse("home:employee-list") + "?username=test_user"
        )
        self.assertEqual(
            list(response.context["employee_list"]),
            list(Employee.objects.filter(username__icontains="test_user"))
        )

    def test_form_valid_with_blank_username(self):
        form_data = {"username": ""}
        form = EmployeeSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_valid_with_valid_username(self):
        form_data = {"username": "johndoe"}
        form = EmployeeSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_with_long_username(self):
        form_data = {"username": "a" * 64}
        form = EmployeeSearchForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_username_field_has_correct_label(self):
        form = EmployeeSearchForm()
        self.assertEqual(form.fields["username"].label, "")


class PositionSearchTests(TestCase):
    def test_search_position_by_name(self):
        response = self.client.get(reverse("home:position-list") + "?name=Test_python")
        self.assertEqual(
            list(response.context["position_list"]),
            list(Position.objects.filter(name__icontains="Test_python")),
        )

    def test_form_valid_with_blank_position(self):
        form_data = {"name": ""}
        form = EmployeeSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_valid_with_valid_name(self):
        form_data = {"name": "test_name"}
        form = EmployeeSearchForm(data=form_data)
        self.assertTrue(form.is_valid())


class TaskTypeSearchTests(TestCase):
    def test_search_task_type_by_name(self):
        response = self.client.get(reverse("home:type-list") + "?name=Test_type")
        self.assertEqual(
            list(response.context["tasktype_list"]),
            list(Position.objects.filter(name__icontains="Test_type")),
        )

    def test_form_valid_with_blank_task_type(self):
        form_data = {"name": ""}
        form = EmployeeSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_valid_with_valid_name(self):
        form_data = {"name": "test_name"}
        form = EmployeeSearchForm(data=form_data)
        self.assertTrue(form.is_valid())


class TaskSearchTests(TestCase):
    def test_search_task_by_name(self):
        response = self.client.get(reverse("home:task-list") + "?name=Test_task")
        self.assertEqual(
            list(response.context["task_list"]),
            list(Position.objects.filter(name__icontains="Test_task")),
        )

    def test_form_valid_with_blank_task(self):
        form_data = {"name": ""}
        form = EmployeeSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_valid_with_valid_name(self):
        form_data = {"name": "test_name"}
        form = EmployeeSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
