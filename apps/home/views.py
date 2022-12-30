from django import template
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse, reverse_lazy
from django.views import generic

from apps.home.forms import (
    EmployeeCreationForm,
    EmployeeUpdateForm,
    TaskCreationForm,
    TaskUpdateForm,
)
from apps.home.models import Task, Employee, Position, TaskType


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


class EmployeeCreateView(generic.CreateView):
    model = Employee
    form_class = EmployeeCreationForm
    success_url = reverse_lazy("home:employee-list")


class EmployeeUpdateView(generic.UpdateView):
    model = Employee
    form_class = EmployeeUpdateForm
    success_url = reverse_lazy("home:employee-list")


class EmployeeDeleteView(generic.DeleteView):
    model = Employee
    success_url = reverse_lazy("home:employee-list")


class EmployeeDetailView(generic.DetailView):
    model = Employee
    template_name = "home/employee_detail.html"


class TaskListView(generic.ListView):
    model = Task
    queryset = Task.objects.all().select_related("task_type").prefetch_related("assignees")
    template_name = "home/task_list.html"


class TaskDetailView(generic.DetailView):
    model = Task
    template_name = "home/task_detail.html"


class TaskCreateView(generic.CreateView):
    model = Task
    form_class = TaskCreationForm
    success_url = reverse_lazy("home:task-list")


class TaskUpdateView(generic.UpdateView):
    model = Task
    form_class = TaskUpdateForm
    success_url = reverse_lazy("home:task-list")


class TaskDeleteView(generic.DeleteView):
    model = Task
    success_url = reverse_lazy("home:task-list")


class TaskTypeListView(generic.ListView):
    model = TaskType
    template_name = "home/type_list.html"


class TaskTypeCreateView(generic.CreateView):
    model = TaskType
    success_url = reverse_lazy("home:type-list")
    fields = "__all__"


class TaskTypeUpdateView(generic.UpdateView):
    model = TaskType
    success_url = reverse_lazy("home:type-list")


class TaskTypeDeleteView(generic.DeleteView):
    model = TaskType
    success_url = reverse_lazy("home:type-list")


class PositionListView(generic.ListView):
    model = Position


class PositionUpdateView(generic.UpdateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("home:position-list")


class PositionCreateView(generic.CreateView):
    model = Position
    fields = "__all__"
    template_name = "home/position_form.html"
    success_url = reverse_lazy("home:position-list")


class PositionDeleteView(generic.DeleteView):
    model = Position
    success_url = reverse_lazy("home:position-list")


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
