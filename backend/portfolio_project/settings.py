from pathlib import Path
import os

# --- Base Directory ---
BASE_DIR = Path(__file__).resolve().parent.parent

# --- Environment Configuration ---
SECRET_KEY = os.environ.get('SECRET_KEY', 'default-local-secret-key-that-is-safe-to-commit')
DEBUG = 'RENDER' not in os.environ

ALLOWED_HOSTS = []
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
else:
    ALLOWED_HOSTS.append('127.0.0.1')

# --- Application Definition ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'content',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'portfolio_project.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates', 'DIRS': [], 'APP_DIRS': True,
        'OPTIONS': { 'context_processors': [ 'django.template.context_processors.debug', 'django.template.context_processors.request', 'django.contrib.auth.context_processors.auth', 'django.contrib.messages.context_processors.messages', ], },
    },
]
WSGI_APPLICATION = 'portfolio_project.wsgi.application'

# --- THE FIX: Simplified Database Configuration for Render ---
# This uses SQLite, which works on Render's free tier by default.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        # Render provides a persistent disk at this location for free tiers
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# --- Password Validation ---
AUTH_PASSWORD_VALIDATORS = [ {'NAME': '...'}, ] # Unchanged

# --- Internationalization ---
LANGUAGE_CODE = 'en-us'; TIME_ZONE = 'UTC'; USE_I18N = True; USE_TZ = True # Unchanged

# --- Static Files ---
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# --- Other Settings ---
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
CORS_ALLOWED_ORIGINS = ["https://satyampote.tech", "http://127.0.0.1:5500", "http://localhost:5500"]
CORS_ALLOWED_ORIGIN_REGEXES = [r"^https://\w+\.onrender\.com$"]