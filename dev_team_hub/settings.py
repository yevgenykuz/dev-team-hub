"""
Django settings for dev-team-hub project.
"""

import os

import dj_database_url
import raven
from decouple import config, Csv
from django.utils.log import DEFAULT_LOGGING

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Debug mode:
DEBUG = config('DEBUG', default=False, cast=bool)

# Admins and managers list for error reporting if DEBUG=False:
TEMP_ADMINS = config('ADMINS', default='', cast=Csv())
TEMP_MANAGERS = config('MANAGERS', default='', cast=Csv())
ADMINS = [(name, email) for name, email in zip(TEMP_ADMINS[0::2], TEMP_ADMINS[1::2])]  # 500 errors
MANAGERS = [(name, email) for name, email in zip(TEMP_MANAGERS[0::2], TEMP_MANAGERS[1::2])]  # 404 errors

# Logging and sentry:
LOG_LEVEL = config('LOG_LEVEL', default='INFO')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': DEFAULT_LOGGING['filters']['require_debug_false'],
        'require_debug_true': DEFAULT_LOGGING['filters']['require_debug_true']
    },
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s] %(name)-16s %(levelname)-8s: %(message)s',
            'datefmt': '%d-%b-%Y %H:%M:%S'
        },
        'django.server': DEFAULT_LOGGING['formatters']['django.server']
    },
    'handlers': {
        'console': {
            'level': LOG_LEVEL,
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'sentry': {
            'level': 'WARNING',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
        'local_file': {
            'level': LOG_LEVEL,
            'filters': ['require_debug_false'],
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': os.path.join(config('LOGS_DIR', default=''), 'hub.log'),
            'maxBytes': 1024 * 1024 * 20,  # 20MB,
            'backupCount': 10,
        },
        'django.server': DEFAULT_LOGGING['handlers']['django.server'],
        'mail_admins': DEFAULT_LOGGING['handlers']['mail_admins'],
    },
    'loggers': {
        '': {
            'handlers': ['console', 'mail_admins', 'sentry', 'local_file'],
            'level': LOG_LEVEL,
        },
        'django.server': {
            'handlers': ['django.server', 'sentry', 'local_file'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}

RAVEN_CONFIG = {
    'dsn': config('SENTRY_DSN', default=''),
    'release': raven.fetch_git_sha(BASE_DIR),
}

# Security:
SECRET_KEY = config('SECRET_KEY')
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())
# X_FRAME_OPTIONS = 'DENY'
# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True
# SECURE_CONTENT_TYPE_NOSNIFF = True
# SECURE_BROWSER_XSS_FILTER = True

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    'django_nose',
    'raven.contrib.django.raven_compat',
    'ckeditor',
    'widget_tweaks',

    'hub.apps.HubConfig',
    'news.apps.NewsConfig',
    'wiki.apps.WikiConfig',
    'forum.apps.ForumConfig',
]

MIDDLEWARE = [
    'django.middleware.common.BrokenLinkEmailsMiddleware',  # send emails to MANAGERS if user got a 404 page
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'dev_team_hub.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'dev_team_hub.wsgi.application'

# Database
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL')
    )
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Chicago'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# The name of the URL pattern to redirect the user to after log in and out:
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'index'
LOGOUT_REDIRECT_URL = 'index'

# Email:
EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = config('EMAIL_HOST', default='')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
DEFAULT_FROM_EMAIL = config('EMAIL_FROM', default='Dev Team <DevTeam@company.com>')
# Error report emails prefix:
SERVER_EMAIL = config('SERVER_EMAIL', default='Dev Team Hub <DevTeamSite@company.com>')
EMAIL_SUBJECT_PREFIX = config('EMAIL_ERROR_REPORT_PREFIX', default='[Dev Team Hub] ')

# Testing:
# Use nose to run all tests
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
# Tell nose to measure coverage
NOSE_ARGS = [
    '--with-coverage',
    '--cover-erase',
    '--cover-package=hub,news,wiki,forum',
]
