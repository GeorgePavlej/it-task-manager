from django.db import models
from django.contrib.auth.models import AbstractUser


class Position(models.Model):
    name = models.CharField(max_length=56)

    def __str__(self) -> str:
        return self.name


class Employee(AbstractUser):
    position = models.ForeignKey(
        Position,
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "employee"
        verbose_name_plural = "employees"

    @property
    def calc_progress(self):
        tasks = self.tasks.all()
        assigned_tasks = self.tasks.count()
        counter_tasks = 0

        if tasks is None or tasks is 0:
            return 0

        for task in tasks:
            if task.is_completed:
                counter_tasks += 1
        result = int((counter_tasks * 100) / assigned_tasks)
        return result

    def __str__(self) -> str:
        return f"{self.username} ({self.first_name} {self.last_name})"


class TaskType(models.Model):
    name = models.CharField(max_length=56)

    def __str__(self) -> str:
        return self.name


class Task(models.Model):

    PRIORITY_CHOICES = [
        (1, "Low"),
        (2, "High"),
        (3, "Urgent"),
    ]

    priority = models.IntegerField(
        choices=PRIORITY_CHOICES,
        default=2
    )

    name = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    deadline = models.DateField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE)
    assignees = models.ManyToManyField(Employee, related_name="tasks")

    def __str__(self) -> str:
        return self.name
