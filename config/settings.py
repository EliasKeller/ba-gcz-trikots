from pathlib import Path
import os

import dj_database_url
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.getenv("SECRET_KEY", "unsafe-dev-key")

DEBUG = os.getenv("DEBUG", "False") == "True"

if os.getenv('DATABASE_URL'):
    ALLOWED_HOSTS = [
        'admin.gcz-trikots.eliaskeller.ch',
        'ba-gcz-trikots-0ceb3b32aac2.herokuapp.com',
    ]
else:
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']


# Application definition
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'cloudinary_storage',
    'django.contrib.staticfiles',
    'cloudinary',
    'trikots',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASE_URL = os.getenv('DATABASE_URL')

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.config(conn_max_age=600)
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DB_NAME'),
            'USER': os.getenv('DB_USER'),
            'PASSWORD': os.getenv('DB_PASSWORD'),
            'HOST': os.getenv('DB_HOST', '127.0.0.1'),
            'PORT': os.getenv('DB_PORT', '5432'),
        }
    }



# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

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


JAZZMIN_SETTINGS = {
    "site_title": "GCZ Trikots",
    "site_header": "GCZ-Trikots",
    "site_brand": "GCZ-Trikots",
    "site_logo": "logo/gcz-trikots-logo.png",
    "login_logo": "logo/gcz-trikots-logo.png",
    "custom_css": "css/custom.css",
    "site_logo_classes": "gcz-logo",

    "welcome_sign": "Willkommen Ruedi",
    "copyright": "© GCZ Trikots",
    "show_sidebar": True,
    "navigation_expanded": True,
    "order_with_respect_to": [
        "trikots.Shirt",
        "trikots.Match",
        "trikots.Club",
        "trikots.League",
        "trikots.Season",
        "trikots.SeasonClub",
        "trikots.Country",
        "trikots.Person",
        "trikots.Supplier",
    ],
    "icons": {
        "auth.User": "fas fa-user-shield",
        "trikots.Match": "fas fa-futbol",
        "trikots.Club": "fas fa-shield-alt",
        "trikots.Country": "fas fa-flag",
        "trikots.League": "fas fa-trophy",
        "trikots.Person": "fas fa-user",
        "trikots.SeasonClub": "fas fa-layer-group",
        "trikots.Season": "fas fa-calendar-alt",
        "trikots.Shirt": "fas fa-tshirt",
        "trikots.Supplier": "fas fa-industry",
    },
}

JAZZMIN_UI_TWEAKS = {

    # =========================
    # THEME (extrem wichtig)
    # =========================
    "theme": "flatly",               # clean modern
    "default_theme_mode": "auto",    # folgt System (dark/light)

    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-outline-secondary",
        "info": "btn-outline-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    }
}

LANGUAGE_CODE = 'de-ch'
TIME_ZONE = 'UTC'
USE_I18N = True

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = BASE_DIR / "staticfiles"

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.getenv('CLOUDINARY_API_KEY'),
    'API_SECRET': os.getenv('CLOUDINARY_API_SECRET'),
}

MEDIA_URL = '/media/'

STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}
# Für django-cloudinary-storage Kompatibilität
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"