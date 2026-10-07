"""
Django settings for sand_aggregates project.
Production-ready configuration with environment variable support.
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env if available
try:
    from dotenv import load_dotenv
    load_dotenv(BASE_DIR / '.env')
except ImportError:
    pass

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'django-insecure-sand-aggregates-key-8c@d92!#8f&491a!zp92*v_k2!lx'
)

# DEBUG should be False in production
DEBUG = os.environ.get('DJANGO_DEBUG', 'True').lower() in ('true', '1', 'yes')

ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1,0.0.0.0,*').split(',')
ALLOWED_HOSTS = [host.strip() for host in ALLOWED_HOSTS if host.strip()]
if '.pythonanywhere.com' not in ALLOWED_HOSTS and '*' not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append('.pythonanywhere.com')

# CSRF trusted origins for secure HTTPS deployments (e.g. PythonAnywhere, custom domain)
csrf_origins = os.environ.get(
    'DJANGO_CSRF_TRUSTED_ORIGINS',
    'https://*.pythonanywhere.com,http://localhost:8000,http://127.0.0.1:8000'
).split(',')
CSRF_TRUSTED_ORIGINS = [origin.strip() for origin in csrf_origins if origin.strip()]

# Honor HTTPS header forwarded by PythonAnywhere and reverse proxies
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Local apps
    'website.apps.WebsiteConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Production static serving
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sand_aggregates.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'website.context_processors.site_context',  # Site-wide business info & categories
            ],
        },
    },
]

WSGI_APPLICATION = 'sand_aggregates.wsgi.application'
ASGI_APPLICATION = 'sand_aggregates.asgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
STATIC_ROOT = BASE_DIR / 'staticfiles'

# WhiteNoise storage: allows local dev caching while ensuring live manifest caching
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage' if not DEBUG else 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Media files (User uploaded images like product photos)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Site Default Settings (overridable via SiteSetting model or env vars)
SITE_DEFAULTS = {
    'BUSINESS_NAME': os.environ.get('BUSINESS_NAME', 'LJ ENTERPRISE'),
    'PHONE_NUMBER': os.environ.get('PHONE_NUMBER', '+91 81413 52886'),
    'PHONE_RAW': os.environ.get('PHONE_RAW', '+918141352886'),
    'WHATSAPP_NUMBER': os.environ.get('WHATSAPP_NUMBER', '918141352886'),
    'EMAIL_ADDRESS': os.environ.get('EMAIL_ADDRESS', 'infoljenterprise07@gmail.com'),
    'ADDRESS': os.environ.get('ADDRESS', 'Ahmedabad, Gujarat, India'),
    'BUSINESS_HOURS': os.environ.get('BUSINESS_HOURS', 'Open 24 hours'),
    'GOOGLE_MAPS_URL': os.environ.get('GOOGLE_MAPS_URL', 'https://www.google.com/maps?q=Ahmedabad,Gujarat,India&output=embed'),
    'INSTAGRAM_URL': os.environ.get('INSTAGRAM_URL', 'https://www.instagram.com/infoljenterprise?stkn=MWd3cGN3dDV6Ym44aA=='),
    'LINKEDIN_URL': os.environ.get('LINKEDIN_URL', 'https://www.linkedin.com/company/rashienterprise'),
}
