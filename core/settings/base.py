"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG') == 'True'

ALLOWED_HOSTS = ['.vercel.app',]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
   

    'prms', # Add the prms app to the installed apps
    'tailwind', # Add the tailwind app to the installed apps
    'theme', # Add the theme app to the installed apps

    # 'compressor' ,
    'django_browser_reload', # Add the django_browser_reload app to the installed apps
    'django_extensions', # Add the django_extensions app to the installed apps
    'django_htmx', # Add the django_htmx app to the installed
    'widget_tweaks', # Add the widget_tweaks app to the installed apps

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]

TAILWIND_APP_NAME = 'theme' # Add the tailwind app name to the TAILWIND_APP_NAME variable

INTERNAL_IPS = [
    "127.0.0.1",
]
NPM_BIN_PATH = 'C:/Program Files/nodejs/npm.cmd' # Add the path to the npm binary

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
     # whitenoise
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "django_browser_reload.middleware.BrowserReloadMiddleware", # Add the BrowserReloadMiddleware to the middleware
    'django_htmx.middleware.HtmxMiddleware', # Add the HtmxMiddleware to the middleware
    "allauth.account.middleware.AccountMiddleware",
    
   
]

ROOT_URLCONF = 'core.urls'

AUTH_USER_MODEL = 'prms.User' # Add the custom user model to the AUTH_USER_MODEL variable

AUTHENTICATION_BACKENDS = [

    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by email
    'allauth.account.auth_backends.AuthenticationBackend',
]

ACCOUNT_FORMS = {
    'signup': 'prms.forms.CustomSignupForm',
}


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': False,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                # Add the global context processor to the context processors list
                'prms.context_processor.global_context_processor',
                
            ],
            'loaders':[(
                'django.template.loaders.cached.Loader', [
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                    'django_components.template_loader.Loader',
                ]
            )],
            'builtins': [
                'django_components.templatetags.component_tags',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases




# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/
STATIC_ROOT = BASE_DIR / "staticfiles"

STATIC_URL = 'theme/' # Change the STATIC_URL variable to 'theme/

STATICFILES_DIRS = [
    BASE_DIR / 'static', 
    BASE_DIR / 'components'
]

STATIC_ROOT = BASE_DIR / 'staticfiles' # Add the STATIC_ROOT variable

MEDIA_URL = '/media/' # Add the MEDIA_URL variable
MEDIA_ROOT = BASE_DIR / 'static/media' # Add the MEDIA_ROOT variable

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# django-allauth settings
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': os.getenv('CLIENT_ID'),
            'secret': os.getenv('CLIENT_SECRET'),
            'key': ''
        },
        'SCOPE': [
            'profile',
            'email',

        ],
    }
}

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_VERIFICATION = True
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
# sender email
DEFAULT_FROM_EMAIL = os.getenv('EMAIL_HOST_USER')

LOGIN_REDIRECT_URL = 'dashboard' # Add the LOGIN_REDIRECT_URL variable
LOGOUT_REDIRECT_URL = 'account_login' # Add the LOGIN_REDIRECT_URL variable


# Email backend

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')  # Replace with your Gmail email
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')  # Replace with your Gmail password