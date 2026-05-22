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
    "itinerary_service.adapters.outbound.db",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
]

if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True
else:
    CORS_ALLOWED_ORIGINS: list[str] = []

ROOT_URLCONF = "itinerary_service.config.urls"
TEMPLATES = []
WSGI_APPLICATION = "itinerary_service.config.wsgi.application"
ASGI_APPLICATION = "itinerary_service.config.asgi.application"

POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "").strip()

if POSTGRES_HOST:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get("POSTGRES_DB", "itineraries"),
            "USER": os.environ.get("POSTGRES_USER", "itineraries_user"),
            "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "itineraries_pass"),
            "HOST": POSTGRES_HOST,
            "PORT": os.environ.get("POSTGRES_PORT", "5432"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

AIRPORT_SERVICE_BASE_URL = os.environ.get("AIRPORT_SERVICE_BASE_URL", "http://127.0.0.1:8001").rstrip("/")

LANGUAGE_CODE = "es-co"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
