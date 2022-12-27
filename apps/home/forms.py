from django.contrib.auth.forms import UserCreationForm
from django import forms
from apps.home.models import Employee, Task


class EmployeeCreationForm(UserCreationForm):

    class Meta:
        model = Employee
        fields = UserCreationForm.Meta.fields + (
            "username",
            "first_name",
            "last_name",
            "email",
            "position",
        )


class EmployeeUpdateForm(forms.ModelForm):

    class Meta:
        model = Employee
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "position",
        )


class TaskCreationForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = (
            "name",
            "description",
            "deadline",
            "task_type",
            "assignees"
        )


class TaskUpdateForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = (
            "name",
            "description",
            "deadline",
            "task_type",
            "assignees"
        )