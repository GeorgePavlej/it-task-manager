from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.home.models import (
    Employee,
    Task,
    TaskType,
    Position,
)


@admin.register(Employee)
class DriverAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("position", "image",)
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("position", "image",)}),)
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                        "license_number",
                        "position",
                        "image",
                    )
                },
            ),
        )
    )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_filter = ("name",)


@admin.register(TaskType)
class TypeAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_filter = ("name",)


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_filter = ("name",)
