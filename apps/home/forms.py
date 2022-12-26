from django.contrib.auth.forms import UserCreationForm
from django import forms
from apps.home.models import Employee


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