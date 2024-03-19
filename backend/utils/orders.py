import json
import logging
import aiohttp
import asyncio
from asgiref.sync import sync_to_async
from celery import shared_task
from django.contrib.auth import get_user_model
from utils.user_tasks import create_user_task

User = get_user_model()
logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.ERROR)

logger = logging.getLogger(__name__)


async def create_item(order_data, url, item_type="order"):
    """
    Create an item using the provided order item, URL, and type.

    Args:
        order_data (Any): The order item to be created, or the response from the clickup API for the Order.
        url (str): The URL to send the request to.
        type (str, optional): The type of item. Defaults to "order".

    Returns:
        None: If there was an error creating the order item.
        Any: The created item if successful.
    """
    async with aiohttp.ClientSession() as session:
        async with session.post(url=url, json=order_data) as response:
            if response.status != 200:
                logger.error(f"Error creating order item: {await response.text()}")
                raise Exception(f"Error creating order item: {await response.text()}")
            try:
                data = await response.text()
                if item_type == "order_item":
                    sync_to_async(create_user_task(data))
            except Exception as e:
                logger.error(f"Failed to decode JSON: {e}")


async def update_clickup_task(order_data, url):
    async with aiohttp.ClientSession() as session:
        async with session.post(url=url, json=order_data) as response:
            if response.status != 200:
                logger.error(f"Error updating order: {await response.text()}")
                raise Exception(f"Error updating order: {await response.text()}")
            try:
                data = await response.text()
            except Exception as e:
                logger.error(f"Failed to decode JSON: {e}")
