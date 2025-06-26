from pathlib import Path
import os
import dj_database_url

# --- Base Directory ---
BASE_DIR = Path(__file__).resolve().parent.parent

# --- Environment Configuration ---
SECRET_KEY = os.environ.get('SECRET_KEY', 'a_strong_default_secret_key_for_local_use')
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

# --- THE FIX: Database Configuration ---
# This is the robust way to configure the database for Render.
DATABASES = {
    'default': dj_database_url.config(
        # Get the database URL from the 'DATABASE_URL' environment variable.
        # This is crucial for the build process on Render.
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600,
        # Enable SSL only when on Render, not for local SQLite.
        ssl_require='RENDER' in os.environ 
    )
}


# --- Password Validation ---
AUTH_PASSWORD_VALIDATORS = [ {'NAME': '...'}, ] # Unchanged

# --- Internationalization ---
LANGUAGE_CODE = 'en-us'; TIME_ZONE = 'UTC'; USE_I18N = True; USE_TZ = True # Unchanged

# --- Static Files ---
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# --- Media Files (Using URLFields now, so no special settings needed) ---

# --- Other Settings ---
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
CORS_ALLOWED_ORIGINS = ["https://satyampote.tech", "http://127.0.0.1:5500", "http://localhost:5500"]
CORS_ALLOWED_ORIGIN_REGEXES = [r"^https://\w+\.onrender\.com$"]