from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.test import TestCase

from apps.home.models import (
    Position,
    Task,
    TaskType,
    Employee,
)


class EmployeeTestCase(TestCase):
    def setUp(self) -> None:
        self.position = Position.objects.create(name="Test Developer")
        self.task_type = TaskType.objects.create(name="Test name")

        self.employee = get_user_model().objects.create_user(
            username="test",
            password="test12345",
            first_name="test first",
            last_name="Test last",
            position=self.position,
        )

    def test_employee_str(self) -> None:
        self.assertEqual(
            str(self.employee),
            f"{self.employee.username} "
            f"({self.employee.first_name} "
            f"{self.employee.last_name})",
        )

    def test_create_employee_with_position(self) -> None:
        self.assertEqual(self.employee.position, self.position)

    def test_image(self) -> None:
        self.assertFalse(self.employee.image)

        self.employee.image.save("test_image.jpg", ContentFile("content"))

        self.assertTrue(self.employee.image)

    def test_calc_progress_when_zero(self) -> None:
        self.assertEqual(self.employee.calc_progress, 0)

    def test_calc_progress_with_three_tasks(self) -> None:
        tasks = [
            Task.objects.create(task_type=self.task_type, is_completed=True),
            Task.objects.create(task_type=self.task_type, is_completed=False),
            Task.objects.create(task_type=self.task_type, is_completed=True),
        ]
        self.employee.tasks.set(tasks)

        self.assertEqual(self.employee.calc_progress, 66)


class PositionTestCase(TestCase):
    def test_position_str(self) -> None:
        position = Position.objects.create(
            name="Test name",
        )

        self.assertEqual(str(position), position.name)


class TaskTypeTestCase(TestCase):
    def test_task_type_str(self) -> None:
        task_type = TaskType.objects.create(
            name="Test name",
        )

        self.assertEqual(str(task_type), task_type.name)


class TaskTestCase(TestCase):
    def setUp(self) -> None:
        self.task_type1 = TaskType.objects.create(name="Test task type1")
        self.task_type2 = TaskType.objects.create(name="Test task type2")
        self.employee1 = Employee.objects.create(username="Test name1")
        self.employee2 = Employee.objects.create(username="Test name2")
        self.task1 = Task.objects.create(
            name="Task 1",
            task_type=self.task_type1,
            is_completed=True,
            deadline=None,
        )
        self.task2 = Task.objects.create(
            name="Task 2",
            task_type=self.task_type2,
            is_completed=False,
            deadline="2023-01-08",
        )
        self.task3 = Task.objects.create(
            name="Task 3",
            task_type=self.task_type1,
            is_completed=False,
            deadline="2023-01-09",
        )
        self.task4 = Task.objects.create(
            name="Task 4",
            task_type=self.task_type2,
            is_completed=True,
            deadline=None,
        )
        self.task2.assignees.add(self.employee1)
        self.task3.assignees.add(self.employee2)
        self.task4.assignees.add(self.employee1)
        self.task4.assignees.add(self.employee2)

    def test_task_fields(self) -> None:
        self.assertEqual(self.task1.name, "Task 1")
        self.assertEqual(self.task1.task_type, self.task_type1)
        self.assertTrue(self.task1.is_completed)
        self.assertIsNone(self.task1.deadline)
        self.assertEqual(self.task2.name, "Task 2")
        self.assertEqual(self.task2.task_type, self.task_type2)
        self.assertFalse(self.task2.is_completed)
        self.assertEqual(self.task2.deadline, "2023-01-08")

    def test_task_str(self) -> None:
        self.assertEqual(str(self.task1), "Task 1")
        self.assertEqual(str(self.task2), "Task 2")
