"""
Django settings for hello project.

Generated by 'django-admin startproject' using Django 5.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import os
import socket
import sys
from distutils.util import strtobool
from pathlib import Path
import rest_framework_simplejwt
from datetime import timedelta


# Build paths inside the project like this: BASE_DIR / "subdir".
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'SECRET_KEY' #os.environ["SECRET_KEY"]

# DEBUG = bool(strtobool(os.getenv("DEBUG", "false")))
DEBUG = True

TESTING = "test" in sys.argv

# https://docs.djangoproject.com/en/5.1/ref/settings/#std:setting-ALLOWED_HOSTS
# allowed_hosts = os.getenv("ALLOWED_HOSTS", ".localhost,127.0.0.1,[::1]")
# ALLOWED_HOSTS = list(map(str.strip, allowed_hosts.split(",")))
allowed_hosts = ['*']
ALLOWED_HOSTS = ['*']
CORS_ALLOW_ALL_ORIGINS = True  # For development only
CORS_ALLOW_CREDENTIALS = True
# Application definitions
# CORS_ALLOWED_ORIGINS = ["*"]



CORS_ALLOWED_ORIGINS = [
    "https://59f5-122-160-55-143.ngrok-free.app",
]




INSTALLED_APPS = [
    "hra_address.apps.HraAddressConfig",
    "hra_tenants.apps.HraTenantsConfig",
    "hra_bank_details.apps.HraBankDetailsConfig",
    "hra_users.apps.HraUsersConfig",
    "hra_reporting_manager.apps.HraReportingManagerConfig",
    "hra_education.apps.HraEducationConfig",
    "hra_experience.apps.HraExperienceConfig",
    "hra_customers.apps.HraCustomersConfig",
    "hra_purchase_orders.apps.HraPurchaseOrdersConfig",
    "hra_invoices.apps.HraInvoicesConfig",
    "hra_timesheets.apps.HraTimesheetsConfig",
    "hra_global_configs.apps.HraGlobalConfigsConfig",
    "hra_lookup.apps.HraLookupConfig",
    "pages.apps.PagesConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt",
    "drf_yasg",
    "corsheaders",
    "hra_auth",
]




REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=100),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,  # This may be causing invalid tokens
    'AUTH_HEADER_TYPES': ('Bearer',),
    'TOKEN_BLACKLIST': True,
}





MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]



SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
            'description': "Enter 'Bearer <your_token>' in the field below.",
        }
    }
}


if not TESTING:
    INSTALLED_APPS = [*INSTALLED_APPS, "debug_toolbar"]
    MIDDLEWARE = [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
        *MIDDLEWARE,
    ]

ROOT_URLCONF = "config.urls"

# Starting with Django 4.1+ we need to pick which template loaders to use
# based on our environment since 4.1+ will cache templates by default.
default_loaders = [
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader",
]



cached_loaders = [("django.template.loaders.cached.Loader", default_loaders)]



TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "loaders": default_loaders if DEBUG else cached_loaders,
        },
    },
]





WSGI_APPLICATION = "config.wsgi.application"

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases




DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}




# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": os.getenv("POSTGRES_DB", "hello"),
#         "USER": os.getenv("POSTGRES_USER", "hello"),
#         "PASSWORD": os.getenv("POSTGRES_PASSWORD", "password"),
#         "HOST": os.getenv("POSTGRES_HOST", "postgres"),
#         "PORT": os.getenv("POSTGRES_PORT", "5432"),
#     }
# }
# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field





DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # noqa: E501
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",  # noqa: E501
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",  # noqa: E501
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",  # noqa: E501
    },
]

# Sessions
# https://docs.djangoproject.com/en/5.1/ref/settings/#sessions
SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"

# Redis
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

# Caching
# https://docs.djangoproject.com/en/5.1/topics/cache/
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": REDIS_URL,
    }
}

# Celery
# https://docs.celeryproject.org/en/stable/userguide/configuration.html
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/
STATIC_URL = "/static/"
STATICFILES_DIRS = ["/public", os.path.join(BASE_DIR, "..", "public")]
STATIC_ROOT = "/public_collected"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Django Debug Toolbar
# https://django-debug-toolbar.readthedocs.io/
if DEBUG:
    # We need to configure an IP address to allow connections from, but in
    # Docker we can't use 127.0.0.1 since this runs in a container but we want
    # to access the toolbar from our browser outside of the container.
    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + [
        "127.0.0.1",
        "10.0.2.2",
    ]

AUTH_USER_MODEL = 'hra_users.User'