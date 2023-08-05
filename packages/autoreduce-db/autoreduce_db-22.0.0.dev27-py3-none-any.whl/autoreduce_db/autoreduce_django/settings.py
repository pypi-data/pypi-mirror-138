"""
Django settings for autoreduce_db project.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
from autoreduce_utils.credentials import DB_CREDENTIALS
from autoreduce_utils.settings import PROJECT_DEV_ROOT

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-pd8%8fgsg*fo#0jvi9@0eh*+i(+vtaou2q@588cjr3=x5+$-r7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [  # Minimal apps required to setup JUST the ORM - (increases ORM setup speed)
    'autoreduce_db.reduction_viewer',
    'autoreduce_db.instrument',
]

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
if "RUNNING_VIA_PYTEST" in os.environ or "PYTEST_CURRENT_TEST" in os.environ:
    if "TESTING_MYSQL_DB" in os.environ:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': "autoreduce",
                'USER': "root",
                'PASSWORD': "password",
                'HOST': "127.0.0.1",
                'PORT': "3306",
            }
        }
    else:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        }
elif "AUTOREDUCTION_PRODUCTION" in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': DB_CREDENTIALS.database,
            'USER': DB_CREDENTIALS.username,
            'PASSWORD': DB_CREDENTIALS.password,
            'HOST': DB_CREDENTIALS.host,
            'PORT': DB_CREDENTIALS.port,
            'OPTIONS': {
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            },
        }
    }

else:  # the default development DB backend
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(PROJECT_DEV_ROOT, "sqlite3.db"),
        }
    }

USE_TZ = True
# Fixes compatibility warnings for Django 3.2+
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
