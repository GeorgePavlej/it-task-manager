from django.contrib import admin

from apps.home.models import Employee, Task, TaskType, Position

admin.site.register(Employee)
admin.site.register(Task)
admin.site.register(TaskType)
admin.site.register(Position)
