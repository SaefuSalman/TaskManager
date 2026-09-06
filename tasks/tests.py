from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Task


class TaskModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="budi", password="testpass123")

    def test_create_task(self):
        task = Task.objects.create(owner=self.user, title="Belajar Django")
        self.assertEqual(str(task), "Belajar Django")
        self.assertEqual(task.status, Task.Status.TODO)
        self.assertEqual(task.priority, Task.Priority.MEDIUM)


class TaskViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="budi", password="testpass123")
        self.other_user = User.objects.create_user(username="siti", password="testpass123")
        self.task = Task.objects.create(owner=self.user, title="Tugas Budi")
        self.other_task = Task.objects.create(owner=self.other_user, title="Tugas Siti")

    def test_list_requires_login(self):
        response = self.client.get(reverse("tasks:task-list"))
        self.assertEqual(response.status_code, 302)  # redirect ke login

    def test_user_only_sees_own_tasks(self):
        self.client.login(username="budi", password="testpass123")
        response = self.client.get(reverse("tasks:task-list"))
        self.assertContains(response, "Tugas Budi")
        self.assertNotContains(response, "Tugas Siti")

    def test_create_task(self):
        self.client.login(username="budi", password="testpass123")
        response = self.client.post(
            reverse("tasks:task-create"),
            {"title": "Tugas Baru", "description": "", "status": "todo", "priority": "medium"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(title="Tugas Baru", owner=self.user).exists())

    def test_cannot_access_other_users_task(self):
        self.client.login(username="budi", password="testpass123")
        response = self.client.get(reverse("tasks:task-detail", kwargs={"pk": self.other_task.pk}))
        self.assertEqual(response.status_code, 404)

    def test_delete_task(self):
        self.client.login(username="budi", password="testpass123")
        response = self.client.post(reverse("tasks:task-delete", kwargs={"pk": self.task.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())
