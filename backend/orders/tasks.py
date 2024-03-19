import os
import asyncio
from celery import shared_task
from utils.orders import create_item
import environ

env = environ.Env()

ORDER_URL = env("ORDER_URL")


ORDER_ITEM_URL = env("ORDER_ITEM_URL")


@shared_task
def process_order(order):
    asyncio.run(create_item(order, ORDER_URL))


@shared_task
def process_order_item(order_item):
    asyncio.run(create_item(order_item, ORDER_ITEM_URL, item_type="order_item"))
