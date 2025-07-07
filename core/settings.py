"""
Django settings for core project.
Generado por 'django-admin startproject' usando Django 5.2.3
"""

from pathlib import Path
import os
import dj_database_url

# BASE
BASE_DIR = Path(__file__).resolve().parent.parent

# DEBUG Y PRODUCCIÓN
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-qi56prrj#3%8y7dnmho_1f_aqpo*cfyunf(sx36f$$b=j6=ths')
DEBUG = False
ALLOWED_HOSTS = ['perrovaca.onrender.com']
CSRF_TRUSTED_ORIGINS = ['https://perrovaca.onrender.com']

# APLICACIONES
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'gestion',
]

# MIDDLEWARE
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # para servir archivos estáticos en producción
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URLS Y WSGI
ROOT_URLCONF = 'veterinario.urls'
WSGI_APPLICATION = 'veterinario.wsgi.application'

# TEMPLATES
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

# BASE DE DATOS (Render con dj_database_url)
DATABASES = {
    'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))
}

# VALIDACIÓN DE CONTRASEÑAS
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# INTERNACIONALIZACIÓN
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ARCHIVOS ESTÁTICOS Y MULTIMEDIA
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # para producción (collectstatic)
STATICFILES_DIRS = [BASE_DIR / 'static']             # para desarrollo
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# REDIRECCIONES DE LOGIN
LOGIN_REDIRECT_URL = 'inicio'
LOGOUT_REDIRECT_URL = 'login'
LOGIN_URL = 'login'

# CLAVE PRIMARIA POR DEFECTO
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
