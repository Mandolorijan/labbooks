"""
Generated by 'django-admin startproject' using Django 3.2.16.
"""

from pathlib import Path

from django.contrib.messages import constants as messages

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "i=d0pz8apxr+0!25lwozu)e$)q*^1k4x=494ga6xi-++67d_*&amp;"

DEBUG = True

ALLOWED_HOSTS = ['*'] if DEBUG else ['138.232.74.41', 'labbooks.at']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'crispy_forms',
    "crispy_bootstrap5",
    'ckeditor',
    'django_crontab',

    'cheminventory',
    'journal',
    'labinventory',
    'massspectra',
    'mscpimporter',

    'clustof',
    'nanoparticles',
    'pulsetube',
    'surftof',
    'snowball',
    'toffy',
    'toffy2',
    'vg',
    'wippi',
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

ROOT_URLCONF = 'labbooks.urls'

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [
        BASE_DIR / 'labbooks' / 'templates'
    ],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        ],
    },
}]

WSGI_APPLICATION = 'labbooks.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'labbooks',
        'USER': 'labbooks',
        'PASSWORD': "P5VINNAZVh2W6luqSvDQOTCQA5NqLgb5n5KMPM3F3rgfo0cjOi5kaDs3n0sfsn",
        'HOST': 'postgres',
        'PORT': '',
    }
}
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'}
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Vienna'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'
# STATIC_ROOT = The absolute path to the directory where collectstatic will collect static files for deployment
STATICFILES_DIRS = [
    BASE_DIR / '_vendor',
    BASE_DIR / 'labbooks' / 'static',
]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

ADMINS = (
    ('FelixD', 'felix.duensing@uibk.ac.at'),
    ('JanM', 'Jan.Mayerhofer@uibk.ac.at'),
)

LOGIN_URL = '/admin/login/'

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'mail_admins': {
#             'level': 'ERROR',
#             'class': 'django.utils.log.AdminEmailHandler'
#         }
#     },
#     'loggers': {
#         'django.request': {
#             'handlers': ['mail_admins'],
#             'level': 'ERROR',
#             'propagate': True,
#         },
#     }
# }

DEFAULT_FROM_EMAIL = 'c744-labbooks@uibk.ac.at'
EMAIL_HOST = 'smtp.uibk.ac.at'

# EXPERIMENTS
SURFTOF_BIGSHARE_DATA_ROOT = "/src/media_surftof_data/"
NANOPARTICLES_PREVIEW_SIZE = 150
TOFFY2_REPLACE_H5_PATH = ('Z:/Experiments/Toffy2/Measurements/RAW-TOFWERK-Data/', "/src/media_toffy2_tofwerk_data/")

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-secondary',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

CRONJOBS = [
    ('42 * * * *', 'labbooks.admin_common.export_tables_csv_all', '>> /src/media/cron.log 2>&1')
]
