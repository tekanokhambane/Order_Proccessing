import base64
from .base import *
import boto3
import environ
from botocore.exceptions import ClientError
import json

env = environ.FileAwareEnv()

INSTALLED_APPS += ["storages"]

DEBUG = False
ALLOWED_HOSTS = env("ALLOWED_HOSTS", "").split(",")

ALLOWED_HOSTS = []
SECRET_KEY = env("SECRET_KEY")
# Redis Configuration
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0

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

SESSION_COOKIE_DOMAIN = env("SESSION_COOKIE_DOMAIN")

CORS_ORIGIN_WHITELIST = [
    "http://localhost:5173",  # or your React app's URL
]

AWS_REGION = "eu-west-2"

ssm = boto3.client("ssm")
secret_key_param = ssm.get_parameter(Name="/Prod/DjangoSecret", WithDecryption=True)
SECRET_KEY = secret_key_param["Parameter"]["Value"]


def get_secret(my_secret_name, region=AWS_REGION):
    ##
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region)
    ##
    try:
        get_secret_value_response = client.get_secret_value(SecretId=my_secret_name)
    except ClientError as e:
        if e.response["Error"]["Code"] == "DecryptionFailureException":
            raise e
        elif e.response["Error"]["Code"] == "InternalServiceErrorException":
            raise e
        elif e.response["Error"]["Code"] == "InvalidParameterException":
            raise e
        elif e.response["Error"]["Code"] == "InvalidRequestException":
            raise e
        elif e.response["Error"]["Code"] == "ResourceNotFoundException":
            raise e
    else:
        if "SecretString" in get_secret_value_response:
            return json.loads(get_secret_value_response["SecretString"])
        else:
            return base64.b64decode(get_secret_value_response["SecretBinary"])


db_creds = get_secret("ProdDBSecret")


bucket_name_param = ssm.get_parameter(Name="/Prod/BucketName")
STATIC_URL = "https://{0}.s3.{1}.amazonaws.com/".format(
    bucket_name_param["Parameter"]["Value"], AWS_REGION
)


AWS_STORAGE_BUCKET_NAME = bucket_name_param["Parameter"]["Value"]
AWS_S3_CUSTOM_DOMAIN = "%s.s3.amazonaws.com" % AWS_STORAGE_BUCKET_NAME
AWS_DEFAULT_ACL = "public-read"


STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"
