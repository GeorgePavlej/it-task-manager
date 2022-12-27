from django.urls import path, re_path
from apps.home import views
from apps.home.views import (
    EmployeeListView,
    EmployeeCreateView,
    EmployeeUpdateView,
    EmployeeDeleteView,
    EmployeeDetailView,
    TaskListView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    TaskTypeListView,
    TaskTypeCreateView,
    TaskTypeUpdateView,
    TaskTypeDeleteView,
    )

urlpatterns = [

    # The home page
    path('', views.index, name='home'),

    # Employee list
    path("employee/", EmployeeListView.as_view(), name="employee-list"),
    path("employee/create/", EmployeeCreateView.as_view(), name="employee-create"),
    path("employee/<int:pk>/update/", EmployeeUpdateView.as_view(), name="employee-update"),
    path("employee/<int:pk>/delete/", EmployeeDeleteView.as_view(), name="employee-delete"),
    path("employee/<int:pk>/", EmployeeDetailView.as_view(), name="employee-detail"),

    # Task List
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/create/", TaskCreateView.as_view(), name="task-create"),
    path("tasks/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path("tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),

    # Task Type List
    path("task-type/", TaskTypeListView.as_view(), name="type-list"),
    path("task-type/create/", TaskTypeCreateView.as_view(), name="type-create"),
    path("task-type/<int:pk>/update/", TaskTypeUpdateView.as_view(), name="type-update"),
    path("task-type/<int:pk>/delete/", TaskTypeDeleteView.as_view(), name="type-delete"),


    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]

app_name = "home"
