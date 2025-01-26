import os
from pathlib import Path
from shutil import which

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Security settings
SECRET_KEY = "django-insecure-your-secret-key"
DEBUG = True
ALLOWED_HOSTS = ["*"]

# Installed apps
INSTALLED_APPS = [
    "daphne",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "myapp",  # app
    "tailwind",  # Tailwind CSS integration
    "channels",  # Channels for WebSocket support
]

# Middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",  # For browser reloads
]

ROOT_URLCONF = "FreelanceFlow.urls"

# Templates configuration
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # Custom template directory
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# WSGI and ASGI configurations
WSGI_APPLICATION = "FreelanceFlow.wsgi.application"
ASGI_APPLICATION = "FreelanceFlow.asgi.application"
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("redis", 6379)],
        },
    },
}

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
        "OPTIONS": {
            "timeout": 30,
        },
    }
}

INTERNAL_IPS = [
    "127.0.0.1",
]

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Localization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

import os

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "staticfiles/images"),
    os.path.join(BASE_DIR, "staticfiles/src"),  # Location of `input.css`
    os.path.join(BASE_DIR, "staticfiles/css"),  # Location of `output.css`
]

STATIC_ROOT = "/staticfiles/"  # Collect all static files for production


# Default auto field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Login and Logout redirect URLs
LOGIN_URL = "/login/"  # Redirect to the login page defined in your app
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/login/"

# Tailwind configuration
TAILWIND_APP_NAME = "myapp"  # Update with your app name
NPM_BIN_PATH = which("npm") or "/usr/bin/npm"  # Ensure NPM is available

# Cache Configuration
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    },
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "DEBUG",  # Change to DEBUG for detailed logs
        },
        "daphne": {
            "handlers": ["console"],
            "level": "DEBUG",  # Debug Daphne logs
        },
        "channels": {
            "handlers": ["console"],
            "level": "DEBUG",
        },
    },
}

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


MONGO_DB_NAME = "freelanceflow"
MONGO_HOST = (
    "mongodb"  # Ako koristite Docker, ovo je ime MongoDB servisa iz docker-compose.yml
)
MONGO_PORT = 27017
MONGO_USERNAME = "root"
MONGO_PASSWORD = "12345"
