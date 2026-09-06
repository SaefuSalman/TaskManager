from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import generic

from .forms import TaskForm
from .models import Task


class OwnerQuerysetMixin(LoginRequiredMixin):
    """
    Memastikan user hanya bisa mengakses task miliknya sendiri.
    Dipakai berulang di beberapa class-based view di bawah supaya
    tidak ada kebocoran data antar user (best practice keamanan dasar).
    """

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)


class TaskListView(OwnerQuerysetMixin, generic.ListView):
    model = Task
    template_name = "tasks/task_list.html"
    context_object_name = "tasks"
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        status = self.request.GET.get("status")
        if status:
            qs = qs.filter(status=status)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["status_choices"] = Task.Status.choices
        context["current_status"] = self.request.GET.get("status", "")
        return context


class TaskDetailView(OwnerQuerysetMixin, generic.DetailView):
    model = Task
    template_name = "tasks/task_detail.html"
    context_object_name = "task"


@login_required
def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.owner = request.user
            task.save()
            messages.success(request, f'Tugas "{task.title}" berhasil dibuat.')
            return redirect("tasks:task-list")
    else:
        form = TaskForm()
    return render(request, "tasks/task_form.html", {"form": form, "mode": "create"})


@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, f'Tugas "{task.title}" berhasil diperbarui.')
            return redirect("tasks:task-detail", pk=task.pk)
    else:
        form = TaskForm(instance=task)
    return render(request, "tasks/task_form.html", {"form": form, "mode": "edit", "task": task})


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    if request.method == "POST":
        title = task.title
        task.delete()
        messages.success(request, f'Tugas "{title}" berhasil dihapus.')
        return redirect("tasks:task-list")
    return render(request, "tasks/task_confirm_delete.html", {"task": task})


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Akun berhasil dibuat. Silakan login.")
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})
