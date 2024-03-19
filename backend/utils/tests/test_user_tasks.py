import unittest
from unittest.mock import patch, MagicMock

from utils.user_tasks import create_user_task, update_user_task


class TestCreateUserTask(unittest.TestCase):

    @patch("accounts.models.User.objects.filter")
    @patch("tasks.models.Task.objects.create")
    def test_create_user_task_valid_data(self, mock_task_create, mock_user_filter):
        mock_user = MagicMock()
        mock_user_filter.return_value.first.return_value = mock_user

        task_data = '{"name": "Test Task", "clickup_id": 123, "clickup_user_id": 456, "priority": 1, "status": "Pending", "content": "Task content", "assignee": "test@example.com"}'

        create_user_task(task_data)

        mock_user_filter.assert_called_once_with(email="test@example.com")
        mock_task_create.assert_called_once_with(
            name="Test Task",
            clickup_id=123,
            clickup_user_id=456,
            priority=1,
            status="Pending",
            content="Task content",
            assignee=mock_user,
        )

    def test_create_user_task_invalid_data_type(self):
        task_data = 123
        with self.assertRaises(ValueError):
            create_user_task(task_data)

    def test_create_user_task_missing_assignee(self):
        task_data = '{"name": "Test Task", "clickup_id": 123, "clickup_user_id": 456, "priority": 1, "status": "Pending", "content": "Task content"}'
        with self.assertRaises(ValueError):
            create_user_task(task_data)

    @patch("accounts.models.User.objects.filter")
    def test_create_user_task_user_not_found(self, mock_user_filter):
        mock_user_filter.return_value.first.return_value = None

        task_data = '{"name": "Test Task", "clickup_id": 123, "clickup_user_id": 456, "priority": 1, "status": "Pending", "content": "Task content", "assignee": "nonexistent@example.com"}'
        with self.assertRaises(ValueError):
            create_user_task(task_data)

    @patch("tasks.models.Task.objects.create")
    def test_create_user_task_error_creating_task(self, mock_task_create):
        mock_task_create.side_effect = Exception("Test exception")

        task_data = '{"name": "Test Task", "clickup_id": 123, "clickup_user_id": 456, "priority": 1, "status": "Pending", "content": "Task content", "assignee": "test@example.com"}'
        with self.assertRaises(Exception):
            create_user_task(task_data)


class TestUpdateUserTask(unittest.TestCase):

    @patch("accounts.models.User.objects.filter")
    @patch("tasks.models.Task.objects.filter")
    @patch("utils.user_tasks.logger.error")
    def test_valid_task_data_existing_user(
        self, mock_logger_error, mock_user_filter, mock_task_filter
    ):
        mock_task_filter.return_value.update.return_value = None
        mock_user = MagicMock()
        mock_user_filter.return_value.first.return_value = mock_user
        task_data = '{"clickup_id": 123, "name": "Task Name", "clickup_user_id": 456, "priority": "High", "status": "In Progress", "content": "Task content", "assignee": "user@example.com"}'
        mock_logger_error.return_value = None

        update_user_task(task_data)

    @patch("accounts.models.User.objects.filter")
    @patch("tasks.models.Task.objects.filter")
    @patch("utils.user_tasks.logger.error")
    def test_valid_task_data_non_existing_user(
        self,
        mock_logger_error,
        mock_user_filter,
        mock_task_filter,
    ):
        mock_user_filter.return_value.first.return_value = None
        task_data = '{"clickup_id": 123, "name": "Task Name", "clickup_user_id": 456, "priority": "High", "status": "In Progress", "content": "Task content", "assignee": "nonexistinguser@example.com"}'
        update_user_task(task_data)
        mock_task_filter.assert_called_once()
        mock_logger_error.assert_not_called()

    def test_invalid_task_data(self):
        task_data = 123  # Not a string

        with self.assertRaises(ValueError):
            update_user_task(task_data)

    def test_missing_assignee_email(self):
        task_data = '{"clickup_id": 123, "name": "Task Name", "clickup_user_id": 456, "priority": "High", "status": "In Progress", "content": "Task content"}'

        with self.assertRaises(ValueError):
            update_user_task(task_data)


if __name__ == "__main__":
    unittest.main()
