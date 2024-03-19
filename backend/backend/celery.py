import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings.dev")

app = Celery("backend")
app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.broker_transport_options = {
    "priority_steps": list(range(20)),
    "sep": ":",
    "queue_order_strategy": "priority",
    "queue_max_priority": 20,
    "queue_default_priority": 5,
    "broker_pool_limit": 20,
    # "broker_connection_timeout": 10,
    "broker_failover_strategy": "round-robin",
    "broker_connection_retry": True,
}

app.autodiscover_tasks()
