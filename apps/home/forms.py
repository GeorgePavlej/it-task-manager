from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.utils import timezone

from apps.home.models import (
    Employee,
    Task,
    Position,
    TaskType,
)


class BaseWidgetForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"style": "border: 2px solid #878787;"})


class EmployeeCreationForm(UserCreationForm, BaseWidgetForm):
    class Meta:
        model = Employee
        fields = UserCreationForm.Meta.fields + (
            "username",
            "first_name",
            "last_name",
            "email",
            "position",
            "image",
        )


class EmployeeUpdateForm(BaseWidgetForm):
    class Meta:
        model = Employee
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "position",
            "image",
        )


class TaskUpdateCreateForm(BaseWidgetForm):

    deadline = forms.DateTimeField(widget=forms.SelectDateWidget)
    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(), widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Task
        fields = "__all__"

    def clean_deadline(self):
        deadline = self.cleaned_data["deadline"]
        if deadline < timezone.now():
            raise forms.ValidationError("The deadline cannot be in the past")
        return deadline


class PositionUpdateCreateForm(BaseWidgetForm):
    class Meta:
        model = Position
        fields = ("name",)


class TypeUpdateCreateForm(BaseWidgetForm):
    class Meta:
        model = TaskType
        fields = ("name",)


class EmployeeSearchForm(forms.Form):
    username = forms.CharField(
        max_length=63,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by username"}),
    )


class PositionSearchForm(forms.Form):
    name = forms.CharField(
        max_length=63,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search"}),
    )


class TaskSearchForm(forms.Form):
    name = forms.CharField(
        max_length=63,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by task name"}),
    )


class TypeSearchForm(forms.Form):
    name = forms.CharField(
        max_length=63,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search"}),
    )
