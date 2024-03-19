from celery import shared_task
import aiohttp
import asyncio
from .models import Product


async def get_products(request):
    # get the products from the Product model use asyncio.run
    products = await Product.objects.all()
