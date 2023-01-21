from django.contrib.auth.forms import UserCreationForm
from django.test import TestCase

from apps.home.models import (
    Position,
    Employee,
    Task,
    TaskType,
)
from apps.home.forms import (
    EmployeeCreationForm,
    TaskUpdateCreateForm,
    PositionUpdateCreateForm,
    TypeUpdateCreateForm,
    BaseWidgetForm,
)


class EmployeeCreationFormTests(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Test Developer")

    def test_employee_creation_form_is_subclass_of_user_creation_form(
        self,
    ) -> None:
        self.assertTrue(issubclass(EmployeeCreationForm, UserCreationForm))
        self.assertTrue(issubclass(EmployeeCreationForm, BaseWidgetForm))

    def test_employee_creation_form_has_correct_model_and_field(self) -> None:
        form = EmployeeCreationForm()

        self.assertEqual(form._meta.model, Employee)
        self.assertEqual(
            form._meta.fields,
            UserCreationForm.Meta.fields
            + (
                "username",
                "first_name",
                "last_name",
                "email",
                "position",
                "image",
            ),
        )

    def test_employee_creation_form_saves_employee_to_database(self) -> None:
        form = EmployeeCreationForm(
            data={
                "username": "test_username",
                "password1": "test1234test",
                "password2": "test1234test",
                "email": "test@test.com",
                "first_name": "Test",
                "last_name": "User",
                "position": self.position,
                "image": None,
            }
        )

        self.assertTrue(form.is_valid())

        form.save()

        self.assertEqual(Employee.objects.count(), 1)
        self.assertEqual(Employee.objects.first().username, "test_username")

    def test_employee_creation_form_handles_invalid_data(self) -> None:
        form = EmployeeCreationForm(
            data={
                "username": "",
                "password1": "test1234test",
                "password2": "test1234test",
                "email": "test@test.com",
                "first_name": "Test first",
                "last_name": "Test last",
                "position": self.position,
                "image": None,
            }
        )

        self.assertFalse(form.is_valid())

        self.assertEqual(form.errors, {"username": ["This field is required."]})


class PositionUpdateCreateFormTests(TestCase):
    def test_position_creation_form_name_is_valid(self) -> None:
        form_data = {
            "name": "test_user",
        }
        form = PositionUpdateCreateForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class TypeUpdateCreateFormTests(TestCase):
    def test_task_type_creation_form_name_is_valid(self) -> None:
        form_data = {
            "name": "test_user",
        }
        form = TypeUpdateCreateForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class TaskUpdateCreateFormTests(TestCase):
    def setUp(self):
        self.task_type = TaskType.objects.create(name="Test task type")

    def test_task_update_create_form_is_subclass_of_base_widget_form(self):
        self.assertTrue(issubclass(TaskUpdateCreateForm, BaseWidgetForm))

    def test_task_update_create_form_has_correct_model(self):
        form = TaskUpdateCreateForm()

        self.assertEqual(form._meta.model, Task)
