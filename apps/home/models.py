from django.db import models
from django.contrib.auth.models import AbstractUser


class Position:
    name = models.CharField(max_length=56)

    def __str__(self) -> str:
        return self.name


class Employee(AbstractUser):
    position = models.ForeignKey(Position, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "employee"
        verbose_name_plural = "employees"

    def __str__(self) -> str:
        return f"{self.username} ({self.first_name} {self.last_name})"


class TaskType:
    name = models.CharField(max_length=56)

    def __str__(self) -> str:
        return self.name


class Task(models.Model):

    PRIORITY_CHOICES = [
        (1, "Urgent"),
        (2, "High"),
        (3, "Low"),
    ]

    priority = models.IntegerField(
        max_length=1,
        choices=PRIORITY_CHOICES,
        default=2)

    name = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    deadline = models.DateTimeField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE)
    assignees = models.ManyToManyField(Employee, related_name="tasks")

    def __str__(self) -> str:
        return self.name
