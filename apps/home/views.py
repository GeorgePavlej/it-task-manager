from django import template
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse, reverse_lazy
from django.views import generic

from apps.home.models import Task, Employee, Position, TaskType
from apps.home.forms import (
    EmployeeCreationForm,
    EmployeeUpdateForm,
    TaskCreationForm,
    TaskUpdateForm,
    EmployeeSearchForm,
    TaskSearchForm,
    TypeSearchForm,
    PositionSearchForm,
)


@login_required(login_url="/login/")
def index(request):
    num_tasks = Task.objects.count()
    num_employees = Employee.objects.count()
    num_positions = Position.objects.count()
    num_types = TaskType.objects.count()

    context = {
        'num_tasks': num_tasks,
        "num_employees": num_employees,
        "num_positions": num_positions,
        "num_types": num_types,
    }

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


class EmployeeListView(generic.ListView):
    model = Employee
    queryset = Employee.objects.all().select_related("position")
    paginate_by = 2
    template_name = "home/employee_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(EmployeeListView, self).get_context_data(**kwargs)

        username = self.request.GET.get("username", "")

        context["search_form"] = EmployeeSearchForm(initial={
            "username": username
        })

        return context

    def get_queryset(self):
        form = EmployeeSearchForm(self.request.GET)
        self.queryset = Employee.objects.all()

        if form.is_valid():
            return self.queryset.filter(
                username__icontains=form.cleaned_data["username"]
            )
        return self.queryset


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
    paginate_by = 2
    template_name = "home/employee_detail.html"


class TaskListView(generic.ListView):
    model = Task
    paginate_by = 2
    queryset = Task.objects.all().select_related("task_type").prefetch_related("assignees")
    template_name = "home/task_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)

        name = self.request.GET.get("name", "")

        context["search_form"] = TaskSearchForm(initial={
            "name": name
        })

        return context

    def get_queryset(self):
        form = TaskSearchForm(self.request.GET)
        self.queryset = Task.objects.all()

        if form.is_valid():
            return self.queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )
        return self.queryset


class TaskDetailView(generic.DetailView):
    model = Task
    paginate_by = 2
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


class TypeListView(generic.ListView):
    model = TaskType
    paginate_by = 2
    template_name = "home/type_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TypeListView, self).get_context_data(**kwargs)

        name = self.request.GET.get("name", "")

        context["search_form"] = TypeSearchForm(initial={
            "name": name
        })

        return context

    def get_queryset(self):
        form = TypeSearchForm(self.request.GET)
        self.queryset = TaskType.objects.all()

        if form.is_valid():
            return self.queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )
        return self.queryset


class TypeCreateView(generic.CreateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("home:type-list")


class TypeUpdateView(generic.UpdateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("home:type-list")


class TypeDeleteView(generic.DeleteView):
    model = TaskType
    success_url = reverse_lazy("home:type-list")


class PositionListView(generic.ListView):
    model = Position
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PositionListView, self).get_context_data(**kwargs)

        name = self.request.GET.get("name", "")

        context["search_form"] = PositionSearchForm(initial={
            "name": name
        })

        return context

    def get_queryset(self):
        form = PositionSearchForm(self.request.GET)
        self.queryset = Position.objects.all()

        if form.is_valid():
            return self.queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )
        return self.queryset


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
