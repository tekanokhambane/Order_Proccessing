import asyncio
from celery import shared_task
from utils.orders import update_clickup_task


TASK_URL = "https://hook.eu2.make.com/7we6jxg56j69id1043k7xf2av81f2otn"


@shared_task
def process_task(order):
    asyncio.run(update_clickup_task(order, TASK_URL))
