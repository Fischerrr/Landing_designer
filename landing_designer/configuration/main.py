from uuid import uuid4
from landing_designer.configuration.debug import DEBUG_TOOLBAR, DEBUG, SILK_ENABLED

import os


PROJECT_NAME = 'landing_designer'
SECRET_KEY = 'oonmzt4zdeh-$0^w!q4@qh5f_lf-+-r6mjiljjdwwf02m$+tqw'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ALLOWED_HOSTS = []

STATIC_ROOT = os.path.join(BASE_DIR, '..', 'assets', 'static')
STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR, '..', 'assets', 'media')
MEDIA_URL = '/media/'

# INTERNAL_APPS - пакеты из папки apps/
# EXTERNAL_APPS -  кастомные пакеты (свои или форки)
# THIRD_PARTY_APPS -  сторонние пакеты
# CORE_APPS - django базовые пакеты

INTERNAL_APPS = [
    'apps.feedback',
    'apps.app_auth',
    'apps.landing',
]

EXTERNAL_APPS = []

THIRD_PARTY_APPS = [
    'ckeditor',
    'ckeditor_uploader',
    'dal',
    'dal_select2',
    'django_ymap',
    'versatileimagefield',
    'scss',
]
CORE_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

INSTALLED_APPS = CORE_APPS + THIRD_PARTY_APPS + EXTERNAL_APPS + INTERNAL_APPS

VERSATILEIMAGEFIELD_SETTINGS = {
    'jpeg_resize_quality': 95,
    'sized_directory_name': '__sized__',
    'filtered_directory_name': '__filtered__',
    'placeholder_directory_name': '__placeholder__',
    'create_images_on_demand': True,
    'image_key_post_processor': None,
    'progressive_jpeg': False
}

MIDDLEWARE = [
    'landing_designer.middleware.SubdomainsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'landing_designer.middleware.CacheControlMiddleware',
]

if DEBUG_TOOLBAR:
    INSTALLED_APPS.append('debug_toolbar')
    MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')

if SILK_ENABLED:
    INSTALLED_APPS.append('silk')
    MIDDLEWARE.append('silk.middleware.SilkyMiddleware', )
    SILKY_INTERCEPT_FUNC = lambda request: request.is_ajax()

ROOT_URLCONF = 'landing_designer.urls'

WSGI_APPLICATION = 'landing_designer.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
]

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
AUTH_USER_MODEL = 'app_auth.AppUser'
LANGUAGE_CODE = 'ru-Ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_L10N = True
USE_TZ = True
CKEDITOR_UPLOAD_PATH = "uplsd/"
CKEDITOR_BASEPATH = "/static/ckeditor/ckeditor/"
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': [
            ['Bold', 'Italic', 'Subscript', 'Superscript'],
        ],
        'height': 200,
        'width': 650,
    },
}

# CELERY_BROKER_URL = 'redis://localhost:6379/1'

TEMPLATES = [
    {
        'APP_DIRS': True,
        'BACKEND': 'django_jinja.backend.Jinja2',
        'DIRS': [os.path.join(BASE_DIR, '..', 'templates')],
        'OPTIONS': {
            'app_dirname': 'templates',
            'auto_reload': DEBUG,
            'autoescape': True,
            'bytecode_cache': {
                'backend': 'django_jinja.cache.BytecodeCache',
                'enabled': False,
                'name': 'default',
            },
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
            ],
            'extensions': [
                'jinja2.ext.do',
                'jinja2.ext.loopcontrols',
                'jinja2.ext.with_',
                'jinja2.ext.i18n',
                'jinja2.ext.autoescape',
                'django_jinja.builtins.extensions.CsrfExtension',
                'django_jinja.builtins.extensions.CacheExtension',
                'django_jinja.builtins.extensions.TimezoneExtension',
                'django_jinja.builtins.extensions.UrlsExtension',
                'django_jinja.builtins.extensions.StaticFilesExtension',
                'django_jinja.builtins.extensions.DjangoFiltersExtension',

            ],
            'globals': {},
            'filters': {},
            'match_extension': '.jinja',
            'newstyle_gettext': True,
            'translation_engine': 'django.utils.translation',
            'undefined': None,

        }
    },
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, '..', 'templates')],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
        },
    }
]
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
        "KEY_PREFIX": "landing_designer"
    }
}

DEFAULT_JINJA2_TEMPLATE_EXTENSION = '.jinja'
ANYMAIL = {
    "MAILGUN_API_KEY": "",
    "MAILGUN_SENDER_DOMAIN": "",
}

EMAIL_BACKEND = 'anymail.backends.mailgun.EmailBackend'
# CELERY_EMAIL_BACKEND = 'anymail.backends.mailgun.EmailBackend'
# POST_OFFICE = {
#     'BACKENDS': {
#         'default': 'djcelery_email.backends.CeleryEmailBackend',
#     },
#     'DEFAULT_PRIORITY': 'now',
#     'BATCH_SIZE': 50,
#     'LOG_LEVEL': 2,
#     'SENDING_ORDER': ['created'],
# }

MANAGERS_GROUP_NAME = 'Менеджер'
INTERNAL_IPS = ['127.0.0.1']
FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'
TOUCH_ID = str(uuid4()).split('-')[-1]
STATICFILES_STORAGE = 'landing_designer.storage.StaticVersionStaticFilesStorage'
