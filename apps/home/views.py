from django import template
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.shortcuts import redirect, get_object_or_404
from django.template import loader
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.http import (
    HttpResponse,
    HttpResponseRedirect,
    HttpRequest,
)

from apps.home.models import (
    Task,
    Employee,
    Position,
    TaskType,
)
from apps.home.forms import (
    EmployeeCreationForm,
    EmployeeUpdateForm,
    TaskUpdateCreateForm,
    PositionUpdateCreateForm,
    TypeUpdateCreateForm,
    EmployeeSearchForm,
    TaskSearchForm,
    TypeSearchForm,
    PositionSearchForm,
)


@login_required(login_url="/login/")
def index(request: HttpRequest) -> HttpResponse:
    num_tasks = Task.objects.count()
    num_employees = Employee.objects.count()
    num_positions = Position.objects.count()
    num_types = TaskType.objects.count()

    context = {
        "num_tasks": num_tasks,
        "num_employees": num_employees,
        "num_positions": num_positions,
        "num_types": num_types,
    }

    html_template = loader.get_template("home/index.html")
    return HttpResponse(html_template.render(context, request))


class EmployeeListView(LoginRequiredMixin, generic.ListView):
    model = Employee
    queryset = Employee.objects.all().select_related("position")
    paginate_by = 5
    template_name = "home/employee_list.html"

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        context = super(EmployeeListView, self).get_context_data(**kwargs)

        username = self.request.GET.get("username", "")

        context["search_form"] = EmployeeSearchForm(
            initial={"username": username}
        )

        return context

    def get_queryset(self) -> QuerySet:
        form = EmployeeSearchForm(self.request.GET)
        self.queryset = Employee.objects.all()

        if form.is_valid():
            return self.queryset.filter(
                username__icontains=form.cleaned_data["username"]
            )
        return self.queryset


class EmployeeCreateView(LoginRequiredMixin, generic.CreateView):
    model = Employee
    form_class = EmployeeCreationForm
    success_url = reverse_lazy("home:employee-list")


class EmployeeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Employee
    form_class = EmployeeUpdateForm
    success_url = reverse_lazy("home:employee-list")


class EmployeeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Employee
    success_url = reverse_lazy("home:employee-list")


class EmployeeDetailView(LoginRequiredMixin, generic.DetailView):
    model = Employee
    paginate_by = 5
    template_name = "home/employee_detail.html"


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    queryset = (
        Task.objects.all().select_related(
            "task_type").prefetch_related("assignees")
    )
    paginate_by = 5
    template_name = "home/task_list.html"

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        context = super(TaskListView, self).get_context_data(**kwargs)

        name = self.request.GET.get("name", "")

        context["search_form"] = TaskSearchForm(initial={"name": name})

        return context

    def get_queryset(self) -> QuerySet:
        form = TaskSearchForm(self.request.GET)
        self.queryset = Task.objects.all()

        if form.is_valid():
            return self.queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )
        return self.queryset


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    paginate_by = 5
    template_name = "home/task_detail.html"


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskUpdateCreateForm
    success_url = reverse_lazy("home:task-list")


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskUpdateCreateForm
    success_url = reverse_lazy("home:task-list")


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("home:task-list")


class TypeListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    paginate_by = 5
    template_name = "home/type_list.html"

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        context = super(TypeListView, self).get_context_data(**kwargs)

        name = self.request.GET.get("name", "")

        context["search_form"] = TypeSearchForm(initial={"name": name})

        return context

    def get_queryset(self) -> QuerySet:
        form = TypeSearchForm(self.request.GET)
        self.queryset = TaskType.objects.all()

        if form.is_valid():
            return self.queryset.filter(name__icontains=form.cleaned_data["name"])
        return self.queryset


class TypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    form_class = TypeUpdateCreateForm
    success_url = reverse_lazy("home:type-list")


class TypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = TaskType
    form_class = TypeUpdateCreateForm
    success_url = reverse_lazy("home:type-list")


class TypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = TaskType
    success_url = reverse_lazy("home:type-list")


class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        context = super(PositionListView, self).get_context_data(**kwargs)

        name = self.request.GET.get("name", "")

        context["search_form"] = PositionSearchForm(initial={"name": name})

        return context

    def get_queryset(self) -> QuerySet:
        form = PositionSearchForm(self.request.GET)
        self.queryset = Position.objects.all()

        if form.is_valid():
            return self.queryset.filter(name__icontains=form.cleaned_data["name"])
        return self.queryset


class PositionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Position
    form_class = PositionUpdateCreateForm
    success_url = reverse_lazy("home:position-list")


class PositionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Position
    form_class = PositionUpdateCreateForm
    template_name = "home/position_form.html"
    success_url = reverse_lazy("home:position-list")


class PositionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Position
    success_url = reverse_lazy("home:position-list")


@login_required
def task_status(
        request: HttpRequest, pk: int, pk2: int) -> HttpResponseRedirect:
    task = get_object_or_404(Task, pk=pk)
    task.is_completed = not task.is_completed
    task.save()
    return redirect("home:employee-detail", pk=pk2)


@login_required
def employee_assign_to_task(
        request: HttpRequest, pk: int) -> HttpResponseRedirect:
    employee = Employee.objects.get(id=request.user.id)
    if Task.objects.get(id=pk) in employee.tasks.all():
        employee.tasks.remove(pk)
    else:
        employee.tasks.add(pk)
    return HttpResponseRedirect(reverse_lazy("home:task-detail", args=[pk]))


@login_required(login_url="/login/")
def pages(request: HttpRequest) -> HttpResponse:
    context = {}
    try:

        load_template = request.path.split("/")[-1]

        if load_template == "admin":
            return HttpResponseRedirect(reverse("admin:index"))
        context["segment"] = load_template

        html_template = loader.get_template("home/" + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template("home/page-404.html")
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template("home/page-500.html")
        return HttpResponse(html_template.render(context, request))
