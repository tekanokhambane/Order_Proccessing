from typing import Any
import unittest
from django.test import TestCase
from unittest.mock import patch
from django.contrib.auth import get_user_model
from tasks.tasks import process_task
from tasks.models import Task
from django.urls import reverse

User = get_user_model()


class TaskAdminUpdateViewTest(TestCase):
    def setUp(self) -> None:
        """
        Set up the test environment by creating a user object with the given parameters.

        :param self: The test case object.
        :return: None.
        """
        self.user = User.objects.create_user(
            username="test_user",
            email="test_userpffoa@example.com",
            password="test_password",
            first_name="Test",
            last_name="User",
        )

    def test_task_update_view(self):
        """
        Test the update view functionality by creating a task, updating it, and checking the response status code.
        """
        task = Task.objects.create(
            name="Test Task",
            assignee=self.user,
            priority="high",
            status="in progress",
            content="test content",
        )
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("admin:tasks_task_change", args=(task.id,)),
            data={
                "name": "Updated Task Name",
                "assignee": self.user,
                "priority": "low",
                "status": "in progress",
                "content": "updated content",
                "_continue": "Save and continue editing",
            },
        )
        self.assertEqual(response.status_code, 302)
        updated_task = Task.objects.get(id=task.id)

    def save_model(self, request, obj, form, change) -> None:
        """
        A description of the entire function, its parameters, and its return types.
        """
        super().save_model(request, obj, form, change)
        if change:
            data = {
                "id": f"{obj.id}",
                "name": f"{obj.name}",
                "clickup_id": f"{obj.clickup_id}",
                "clickup_user_id": f"{obj.clickup_user_id}",
                "priority": f"{obj.priority}",
                "status": f"{obj.status}",
                "content": f"{obj.content}",
            }
