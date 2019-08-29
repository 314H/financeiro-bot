"""
Django settings for base_site project.

Generated by 'django-admin startproject' using Django 2.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import datetime
import os

from base_site.database import S_ALLOWED_HOSTS
from base_site.database import S_DATABASES
from base_site.database import S_DEBUG
from base_site.database import S_LOGGING_FILE
from base_site.database import S_SECRET_KEY
from base_site.database import S_SERVICE_ACCOUNT_FILE
from base_site.database import S_TELEGRAM_TOKEN

DATABASES = S_DATABASES
DEBUG = S_DEBUG
SERVICE_ACCOUNT_FILE = S_SERVICE_ACCOUNT_FILE
TELEGRAM_TOKEN = S_TELEGRAM_TOKEN
ALLOWED_HOSTS = S_ALLOWED_HOSTS


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = S_SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True  # on database.py


# Application definition

INSTALLED_APPS = [
    "mainapp",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",  # http://whitenoise.evans.io/en/stable/django.html#using-whitenoise-in-development
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_swagger",
    "django_filters",
    "django_q",
    "import_export",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "base_site.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "base_site.wsgi.application"


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = "pt-br"

TIME_ZONE = "America/Sao_Paulo"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/


STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "botfinanceiro/static")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

GOOGLE_SPREADSHEET_ID = "1yO24GqWCwEW3uFHtqoqTvWgSsvZlQfi5QufTqPZq378"
GOOGLE_RANGE_NAME = "Fluxo Caixa!A1050:I"


REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_jwt.authentication.JSONWebTokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
}

JWT_AUTH = {"JWT_ALLOW_REFRESH": True, "JWT_EXPIRATION_DELTA": datetime.timedelta(seconds=604800)}

Q_CLUSTER = {
    "name": "Schedule",
    "workers": 1,
    "timeout": 30,
    "retry": 600,
    "queue_limit": 50,
    "bulk": 10,
    "orm": "default",
}

LOGIN_URL = "/ricardo/login/"


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
            "class": "logging.FileHandler",
            "filename": S_LOGGING_FILE,
        }
    },
    "loggers": {"": {"handlers": ["file"], "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"), "propagate": True}},
}
