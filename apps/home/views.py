# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic

from apps.home.models import Task, Employee, Position


@login_required(login_url="/login/")
def index(request):
    num_tasks = Task.objects.count()
    num_employees = Employee.objects.count()
    num_positions = Position.objects.count()

    context = {
        'num_tasks': num_tasks,
        "num_employees": num_employees,
        "num_positions": num_positions
    }

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


class EmployeeListView(generic.ListView):
    model = Employee
    queryset = Employee.objects.all().select_related("position")
    template_name = "home/employee_list.html"


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
