import asyncio
from celery import shared_task
from utils.orders import update_clickup_task
import environ

env = environ.Env()

TASK_URL = env("TASK_URL")


@shared_task
def process_task(order):
    asyncio.run(update_clickup_task(order, TASK_URL))
