from django.urls import path

from . import views

app_name = "tasks"

urlpatterns = [
    path("", views.TaskListView.as_view(), name="task-list"),
    path("new/", views.task_create, name="task-create"),
    path("<int:pk>/", views.TaskDetailView.as_view(), name="task-detail"),
    path("<int:pk>/edit/", views.task_update, name="task-update"),
    path("<int:pk>/delete/", views.task_delete, name="task-delete"),
]
