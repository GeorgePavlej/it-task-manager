from django.urls import path, re_path
from apps.home import views
from apps.home.views import (
    EmployeeListView,
    EmployeeCreateView,
    EmployeeUpdateView,
    EmployeeDetailView,
    )

urlpatterns = [

    # The home page
    path('', views.index, name='home'),

    # Employee list
    path("employee/", EmployeeListView.as_view(), name="employee-list"),
    path("employee/create/", EmployeeCreateView.as_view(), name="employee-create"),
    path("employee/<int:pk>/update/", EmployeeUpdateView.as_view(), name="employee-update"),
    path("employee/<int:pk>/", EmployeeDetailView.as_view(), name="employee-detail"),


    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]

app_name = "home"
