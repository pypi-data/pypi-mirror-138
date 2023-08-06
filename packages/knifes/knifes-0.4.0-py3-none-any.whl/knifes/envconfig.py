from decouple import config as c
from django.conf import settings


# 结合decouple和django的settings
def config(key):
    return c(key, default=settings.DEFAULT_ENV_CONFIG_DICT.get(key))
