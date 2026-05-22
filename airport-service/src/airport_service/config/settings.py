import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DEBUG = True
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-only-insecure-key")
if not DEBUG and not os.getenv("DJANGO_SECRET_KEY"):
    raise ImproperlyConfigured(
        "DJANGO_SECRET_KEY debe estar definida en produccion (DEBUG=False)."
    )
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "corsheaders",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
]

# MVP (HU-A3): el mapa web se sirve en otro origen; en depuracion se permite cualquier origen.
if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True
else:
    CORS_ALLOWED_ORIGINS: list[str] = []

ROOT_URLCONF = "airport_service.config.urls"
TEMPLATES = []
WSGI_APPLICATION = "airport_service.config.wsgi.application"
ASGI_APPLICATION = "airport_service.config.asgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

LANGUAGE_CODE = "es-co"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
