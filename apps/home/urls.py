# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views
from apps.home.views import EmployeeListView

urlpatterns = [

    # The home page
    path('', views.index, name='home'),

    # Employee list
    path("employee/", EmployeeListView.as_view(), name="employee-list"),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
