from .base import *

DEBUG = True
CORS_ALLOW_ALL_ORIGINS = True
ROOT_URLCONF = "backend.urls"
ALLOWED_HOSTS = []
REDIS_HOST = "redis"
REDIS_PORT = 6379
REDIS_DB = 0

SECRET_KEY = "django-insecure-dm2zvb=q!vh0mct^^2h6o^u8rb=xl%r3)b_8)!#6sls7ld$#e4"
# Redis Configuration
CELERY_BROKER_URL = (
    f"redis://{REDIS_HOST}:6379/0"  # Example using Redis as the Celery broker
)
CELERY_RESULT_BACKEND = (
    f"redis://{REDIS_HOST}:6379/0"  # Example using Redis as the Celery result backend
)


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        "KEY_PREFIX": "products",
    }
}


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "orderprocess",
        "USER": "tekano",
        "PASSWORD": "mypassword",
        "HOST": "mysql",  # Or an IP Address that your DB is hosted on
        "PORT": "3306",
    }
}

CORS_ORIGIN_WHITELIST = [
    "http://localhost:5173",  # or your React app's URL
]

SESSION_COOKIE_DOMAIN = "127.0.0.1"
