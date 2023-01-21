from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.home.models import Employee, Task, TaskType, Position


EMPLOYEE_URL = reverse("home:employee-list")
TASK_URL = reverse("home:task-list")
TASK_TYPE_URL = reverse("home:type-list")
POSITION_URL = reverse("home:position-list")


class PublicEmployeeTests(TestCase):
    def test_list_login_required(self) -> None:
        response = self.client.get(EMPLOYEE_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateEmployeeTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password123",
        )
        self.client.force_login(self.user)

    def test_retrieve_employees(self) -> None:
        Employee(username="test_name1")
        Employee(username="test_name2")

        response = self.client.get(EMPLOYEE_URL)

        employee = Employee.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["employee_list"]), list(employee))

        self.assertTemplateUsed(response, "home/employee_list.html")


class PublicPositionTest(TestCase):
    def test_list_login_required(self) -> None:
        response = self.client.get(POSITION_URL)

        self.assertEqual(response.status_code, 200)


class PrivatePositionTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password123",
        )
        self.client.force_login(self.user)

    def test_retrieve_positions(self) -> None:
        Position.objects.create(
            name="Test name",
        )

        response = self.client.get(POSITION_URL)

        positions = Position.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["position_list"]), list(positions))

        self.assertTemplateUsed(response, "home/position_list.html")


class PrivateTaskTypeTest(TestCase):
    def test_list_login_required(self) -> None:
        response = self.client.get(TASK_TYPE_URL)

        self.assertEqual(response.status_code, 200)


class PublicTaskTypeTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password123",
        )
        self.client.force_login(self.user)

    def test_retrieve_task_types(self) -> None:
        TaskType.objects.create(
            name="Test name",
        )

        response = self.client.get(TASK_TYPE_URL)

        task_types = TaskType.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["tasktype_list"]), list(task_types))

        self.assertTemplateUsed(response, "home/type_list.html")


class PrivateTaskTest(TestCase):
    def test_list_login_required(self) -> None:
        response = self.client.get(TASK_URL)

        self.assertEqual(response.status_code, 200)


class PublicTaskTest(TestCase):
    def setUp(self) -> None:
        self.task_type = TaskType.objects.create(name="Test type")
        self.user = get_user_model().objects.create_user(
            "test",
            "password123",
        )
        self.client.force_login(self.user)

    def test_retrieve_task(self) -> None:
        Task.objects.create(name="Test name", task_type=self.task_type)

        response = self.client.get(TASK_URL)

        tasks = Task.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["task_list"]), list(tasks))

        self.assertTemplateUsed(response, "home/task_list.html")
