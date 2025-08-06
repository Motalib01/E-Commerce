import os
from pathlib import Path
from decouple import config, Csv  # pip install python-decouple
from django.utils.translation import gettext_lazy as _

BASE_DIR = Path(__file__).resolve().parent.parent

# === Security ===
SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", cast=bool)
ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

GOOGLE_SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, config("GOOGLE_SERVICE_ACCOUNT_FILE"))
GOOGLE_CLIENT_SECRET_FILE = os.path.join(BASE_DIR, 'credentials/client_secret_577784229752-l918ioee4s60vhnl55r1ltlar49imufn.apps.googleusercontent.com.json') 
GOOGLE_REDIRECT_URI = 'http://localhost:8000/oauth2callback/'

# === Custom User Model ===
AUTH_USER_MODEL = "accounts.User"

# === REST Framework ===
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

# === Media files ===
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# === Static files ===
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# === Applications ===
INSTALLED_APPS = [
    # Django apps
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd-party apps
    'rest_framework',
    'corsheaders',
    'drf_yasg',

    # Local apps
    'accounts',
    'catalog',
    'orders',
]

# === Middleware ===
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    # Enable language switching
    'django.middleware.locale.LocaleMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# === URLs and Templates ===
ROOT_URLCONF = 'ecommerce.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],  # ✅ Fixed: Added comma here
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # Required by admin
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ecommerce.wsgi.application'

# === PostgreSQL Database ===
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config("DB_NAME"),
        'USER': config("DB_USER"),
        'PASSWORD': config("DB_PASSWORD"),
        'HOST': config("DB_HOST", default="localhost"),
        'PORT': config("DB_PORT", default="5432"),
    }
}

# === Localization ===
LANGUAGE_CODE = 'en'

LANGUAGES = [
    ('en', _('English')),
    ('fr', _('French')),
    ('ar', _('Arabic')),
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# === CORS Settings ===
CORS_ALLOW_ALL_ORIGINS = True

# === Auto Field ===
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
