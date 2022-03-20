import os
import typing as tp
from datetime import timedelta

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', default='some_secret_key')  # type: ignore

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.environ.get('DEBUG', default=1))  # type: ignore

ALLOWED_HOSTS: tp.List[str] = os.environ.get('ALLOWED_HOSTS', default='*').split(',')  # type: ignore

# CORS settings
CORS_ALLOWED_ORIGINS: tp.List[str] = os.environ.get('CORS_ALLOWED_ORIGINS', default='').split(',')  # type: ignore

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'corsheaders',

    'drf_yasg',

    'rest_framework',

    'api.video',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',

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

# REST FRAMEWORK settings
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_PERMISSIONS_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
    ),
}

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

# JWT SETTINGS
ACCESS_TOKEN_EXPIRE_MINUTES: tp.Optional[int] = int(os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES'))  # type: ignore
REFRESH_TOKEN_EXPIRE_MINUTES: tp.Optional[int] = int(os.environ.get('REFRESH_TOKEN_EXPIRE_MINUTES'))  # type: ignore
DEFAULT_ACCESS_TOKEN_EXPIRE_MINUTES = 180
DEFAULT_REFRESH_TOKEN_EXPIRE_MINUTES = 360
TOKEN_TYPE: tp.Optional[str] = os.environ.get('TOKEN_TYPE')
TOKEN_ALGORITHM: tp.Optional[str] = os.environ.get('TOKEN_ALGORITHM')

# SIMPLE JWT SETTINGS
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES or DEFAULT_ACCESS_TOKEN_EXPIRE_MINUTES),
    'REFRESH_TOKEN_LIFETIME': timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES or DEFAULT_REFRESH_TOKEN_EXPIRE_MINUTES),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': TOKEN_ALGORITHM,
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': (TOKEN_TYPE,),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

# Aws settings
BUCKET_REGION = os.environ.get('BUCKET_REGION', default='test_region')  # type: ignore
VIDEOS_BUCKET = os.environ.get('VIDEOS_BUCKET', default='test_bucket')  # type: ignore
BUCKET_PATH = f'https://s3-{BUCKET_REGION}.amazonaws.com/{VIDEOS_BUCKET}/' + '{}'

BASE_DATETIME_FORMAT = '%Y-%m-%d:%H-%M-%S.%f'

# Internationalization
LANGUAGE_CODE = 'en-us'

TIME_ZONE = os.environ.get('TIME_ZONE', default='Europe/Moscow')  # type: ignore

USE_I18N = True

USE_L10N = True

USE_TZ = True


# STATIC FILES
STATIC_URL = "/staticfiles/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
