"""
Django settings for _op1 project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from decouple import config
from pathlib import Path
from django.utils.translation import gettext_lazy as _
from django.contrib.messages import constants as messages

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    # default
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # third party libraries
    'debug_toolbar',
    'django_editorjs',
    'django_htmx',
    'django_mptt_admin',
    'django_tables2',
    'django_select2',
    'django_xworkflows',
    'import_export',
    'mptt',
    'simple_history',
    'smart_selects',
    'storages',
    'widget_tweaks',
    # internal
    'main.apps.MainConfig',
    'abidan',
    'tipitaka',
    'padanukkama',
    'setting'
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django_htmx.middleware.HtmxMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
]

ROOT_URLCONF = '_op1.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = '_op1.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config("DATABASE_NAME"),
        'USER': config("DATABASE_USER"),
        'PASSWORD': config("DATABASE_PASSWORD"),
        'HOST': config("DATABASE_HOST"),
        'PORT': config("DATABASE_PORT"),
    }
}

# Check database connection
# print('running on db : ' + connection.settings_dict['NAME'])

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'th'

LANGUAGES = [
    ('en', _('English')),
    ('th', _('Thai')),
]

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_ROOT = BASE_DIR / 'public/static'
STATICFILES_DIRS = [
    BASE_DIR / 'static'
]
STATIC_URL = '/static/'

MEDIA_ROOT = BASE_DIR / 'public/uploads'
MEDIA_URL = '/files/'

AWS_STORAGE_BUCKET_NAME = "openpali"
AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")

AWS_S3_ENDPOINT_URL = "https://sgp1.digitaloceanspaces.com"
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400",
     "ACL": "public-read"
}
AWS_LOCATION = "https://openpali.sgp1.digitaloceanspaces.com"

STATICFILES_FOLDER = "static"
MEDIAFILES_FOLDER = "media"

STATICFILES_STORAGE = "custom_storages.StaticFileStorage"
DEFAULT_FILE_STORAGE = "custom_storages.MediaFileStorage"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# auth settings
LOGIN_URL = "/login"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/login"


# JQUERY_URL = True
USE_DJANGO_JQUERY = True


# MESSAGE_TAGS
MESSAGE_TAGS = {
    messages.DEBUG: 'w3-blue-grey',
    messages.INFO: 'w3-pale-blue',
    messages.SUCCESS: 'w3-pale-green',
    messages.WARNING: 'w3-pale-yellow',
    messages.ERROR: 'w3-pale-red',
}


INTERNAL_IPS = [
    "localhost",
    "127.0.0.1",
    # ...
]


# *** NOTE ***
# *** DUMP DATABASE COMMAND => SERVER : op1 op1_dev1***
# $ pg_dump -Fc -h 127.0.0.1 -U op1 op1 -f op1.dump
# *** RESTORE DATABASE COMMAND ***
# sudo -u postgres psql
# DROP DATABASE op1_dev1;
# CREATE DATABASE op1_dev1;
# GRANT ALL PRIVILEGES ON DATABASE op1_dev1 TO op1;
# \q
# $ pg_restore -d op1_dev1 -h 127.0.0.1 -U op1 op1.dump

# *** BACKUP DATABASE COMMAND => SERVER TO LOCAL : op1 to op1
# FROM PGADMIN BACKUP FROM SERVER => RESTORE TO LOCAL
# 1. BACKUP DATABASE op1 (SERVER SIDE)
# 2. FTP DOWNLOAD op1 FROM SERVER
# 3. DROP op1 (if exists) ON LOCAL
# 4. CREATE DATABASE op1 =>
# 2. RESTORE DATABASE op1.sql => sudo -u postgres pg_restore -U postgres -d op1 -1 op1.sql