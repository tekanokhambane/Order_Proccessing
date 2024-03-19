from typing import Any
from django.contrib import admin
from django.contrib.auth import get_user_model
from django import forms
from .models import Task
from .tasks import process_task

User = get_user_model()


class TaskForm(forms.ModelForm):
    assignee = forms.ModelChoiceField(queryset=User.objects.filter(is_staff=True))

    class Meta:
        model = Task
        fields = ["name", "assignee", "priority", "status", "content"]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = [
        "assignee",
        "name",
        "clickup_id",
        "clickup_user_id",
        "priority",
        "status",
        "created_at",
    ]
    form = TaskForm

    def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None:
        super().save_model(request, obj, form, change)
        if change:
            data = {
                "id": f"{obj.id}",
                "name": f"{obj.name}",
                "clickup_id": f"{obj.clickup_id}",
                # "clickup_user_id": f"{obj.clickup_user_id}",
                "priority": f"{obj.priority}",
                "status": f"{obj.status}",
                "content": f"{obj.content}",
            }
            process_task.delay(data)
