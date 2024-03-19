import os
import asyncio
from celery import shared_task
from utils.orders import create_item


ORDER_URL = "https://hook.eu2.make.com/eqrb308y8smy0la3xs1pjpq3rksf2hae"


ORDER_ITEM_URL = "https://hook.eu2.make.com/2w5s0ugfz52e5by5nv4nlposlo2mmubz"


@shared_task
def process_order(order):
    asyncio.run(create_item(order, ORDER_URL))


@shared_task
def process_order_item(order_item):
    asyncio.run(create_item(order_item, ORDER_ITEM_URL, item_type="order_item"))
