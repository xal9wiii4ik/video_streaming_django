import os
import typing as tp

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG')

ALLOWED_HOSTS: tp.List[str] = os.environ.get('ALLOWED_HOSTS').split(',')  # type: ignore


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',

    'api.video',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'base.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'base.wsgi.application'


# Database
SQL_ENGINE = os.environ.get("SQL_ENGINE", default="django.db.backends.sqlite3")  # type: ignore
SQL_DATABASE = os.environ.get("RDS_DB_NAME", default=os.path.join(BASE_DIR, "db.sqlite3"))  # type: ignore
SQL_USER = os.environ.get("RDS_USERNAME", default="user")  # type: ignore
SQL_PASSWORD = os.environ.get("RDS_PASSWORD", default="password")  # type: ignore
SQL_HOST = os.environ.get("RDS_HOSTNAME", default="localhost")  # type: ignore
SQL_PORT = os.environ.get("RDS_PORT", default="5432")  # type: ignore

DATABASES = {
    "default": {
        "ENGINE": SQL_ENGINE,
        "NAME": SQL_DATABASE,
        "USER": SQL_USER,
        "PASSWORD": SQL_PASSWORD,
        "HOST": SQL_HOST,
        "PORT": SQL_PORT,
    }
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


# Aws settings
BUCKET_REGION = os.environ.get('BUCKET_REGION')
VIDEOS_BUCKET = os.environ.get('VIDEOS_BUCKET')

# Internationalization
LANGUAGE_CODE = 'en-us'

TIME_ZONE = os.environ.get('TIME_ZONE', default='Europe/Moscow')  # type: ignore

USE_I18N = True

USE_L10N = True

USE_TZ = True


# STATIC FILES
STATIC_URL = "/staticfiles/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")


# MEDIA FILES
MEDIA_URL = "/mediafiles/"
MEDIA_ROOT = os.path.join(BASE_DIR, "mediafiles")
