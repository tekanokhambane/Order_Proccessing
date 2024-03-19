from django.db import models
from orders.models import Order, OrderItem
from django.contrib.auth import get_user_model

User = get_user_model()


class Task(models.Model):
    class StatusChoices(models.TextChoices):
        IN_PROGRESS = "in progress"
        COMPLETED = "completed"
        DEFERRED = "deferred"
        PENDING = "pending"
        PACKAGED = "packaged"
        INSTALLED = "installed"
        ASSESSMENT = "assessment"

    class PriorityChoices(models.TextChoices):
        URGENT = "urgent"
        HIGH = "high"
        NORMAL = "normal"
        LOW = "low"

    assignee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    name = models.CharField(max_length=255)
    clickup_id = models.CharField(max_length=255, editable=False)
    clickup_user_id = models.CharField(
        max_length=255, editable=False, null=True, blank=True
    )
    priority = models.CharField(
        max_length=255,
        choices=PriorityChoices.choices,
        default=PriorityChoices.NORMAL,
    )
    status = models.CharField(
        max_length=255, choices=StatusChoices.choices, default="pending"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}  {self.priority} {self.status} "
