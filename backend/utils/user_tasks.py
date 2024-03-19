import json
import logging
from django.contrib.auth import get_user_model
from django.db import transaction
from tasks.models import Task


User = get_user_model()
logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


def create_user_task(task_data):
    """
    Creates a task based on the provided task data.

    Args:
        task_data (str): A JSON string containing task details.

    Raises:
        ValueError: If task_data is not a string or if the user is not found.
    """
    if not isinstance(task_data, str):
        raise ValueError("task_data must be a string")

    json_data = json.loads(task_data)

    user_email = json_data.get("assignee")
    if not user_email:
        logger.error("Assignee email is missing in task data")
        raise ValueError("Assignee email is required")

    user = User.objects.filter(email=user_email).first()
    if user is None:
        logger.error(f"User not found with email: {user_email}")
        raise ValueError(f"User not found with email: {user_email}")

    try:
        with transaction.atomic():
            new_task = Task.objects.create(
                name=json_data["name"],
                clickup_id=json_data["clickup_id"],
                clickup_user_id=json_data["clickup_user_id"],
                priority=json_data["priority"],
                status=json_data["status"],
                content=json_data["content"],
                assignee=user,
            )
            logger.info(f"New task created with ID: {new_task.pk}")
    except Exception as e:
        logger.error(f"Error creating task: {e}")
        raise


def update_user_task(task_data):
    """
    Updates a task based on the provided task data.

    Args:
        task_data (str): A JSON string containing task details.

    Raises:
        ValueError: If task_data is not a string or if the user is not found.
    """
    if not isinstance(task_data, str):
        raise ValueError("task_data must be a string")

    json_data = json.loads(task_data)

    user_email = json_data.get("assignee")
    if not user_email:
        logger.error("Assignee email is missing in task data")
        raise ValueError("Assignee email is required")

    user = User.objects.filter(email=user_email).first()
    if user is None:
        logger.error(f"User not found with email: {user_email}")
        raise ValueError(f"User not found with email: {user_email}")

    try:
        with transaction.atomic():
            Task.objects.filter(clickup_id=json_data["clickup_id"]).update(
                name=json_data["name"],
                clickup_id=json_data["clickup_id"],
                clickup_user_id=json_data["clickup_user_id"],
                priority=json_data["priority"],
                status=json_data["status"],
                content=json_data["content"],
                assignee=user,
            )
            logger.info(f"Task updated with ID: {json_data['clickup_id']}")
    except Exception as e:
        logger.error(f"Error updating task: {e}")
        raise
