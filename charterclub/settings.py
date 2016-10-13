"""
Django settings for charterclub project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('CHARTER_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
 

# if this is true, get_username(request) will return testuser. use for
# testing when CAS is not available
CAS_DISABLED = False

TEMPLATE_DEBUG = False

# TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), "templates").replace(
#     "\\","/"),)

# Needed for Django Flatpages
SITE_ID = 2

# For managing templates
TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), "..", "templates").replace('\\', '/'),)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': TEMPLATE_DIRS,
        'APP_DIRS': True,
        'OPTIONS': {
            # ... some options here ...
        },
    },
]


ALLOWED_HOSTS = [
    '.princetoncharterclub.org',
    'localhost',
    '.charterclub.org',
	'.herokuapp.com'
]

CRISPY_TEMPLATE_PACK = 'bootstrap3'

CART_PRODUCT_MODEL = 'gear.models.GearItem' 

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.flatpages',
    'django.contrib.formtools',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'jquery',
    'dajaxice',
    'dajax',
    'charterclub',
    'crispy_forms',
    'carton',
    'events',
    'gear',
    'recruitment',
    'menus',
    'feedback',
    'kitchen',
    'settings_charter',
    'django_bootstrap_calendar',
    'storages', # For AWS
    
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    # required for CAS
    'django_cas.middleware.CASMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'chromelogger.DjangoMiddleware'
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages'
)

# needed for CAS
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'django_cas.backends.CASBackend',
)

ROOT_URLCONF = 'charterclub.urls'

WSGI_APPLICATION = 'charterclub.wsgi.application'

# CAS settings
CAS_SERVER_URL = 'https://fed.princeton.edu/cas/'
CAS_LOGOUT_COMPLETELY = False
CAS_REDIRECT_URL = 'templates/hello.html'

# email backend
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' 
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get('EMAIL_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# FOR IMAGES
ENV_PATH = os.path.abspath(os.path.dirname(__file__))



# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
ON_HEROKU = os.environ.get('ON_HEROKU')
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # WAS 'django.db.backends.sqlite3',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),  # Or path to database file if using sqlite3.
        'NAME': os.environ.get('DB_NAME'),
        # The following settings are not used with sqlite3:
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': '5432',                      # Set to empty string for default.
    }
}

if ON_HEROKU:
    # recommend heroku settings for databases at <https://devcenter.heroku.com/articles/getting-started-with-django>
    import dj_database_url
    DATABASES['default'] =  dj_database_url.config()

    # Honor the 'X-Forwarded-Proto' header for request.is_secure()
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

    # Allow all host headers
    ALLOWED_HOSTS = ['*']
    # Static asset configuration
    import os
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'US/Eastern'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

# STATIC_URL = '/static/'
# From https://django-storages.readthedocs.org/en/latest/backends/amazon-S3.html
AWS_STORAGE_BUCKET_NAME = os.environ['S3_BUCKET_NAME']
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
# STATIC_URL='http://your_s3_bucket.s3.amazonaws.com/%s/' % AWS_STORAGE_BUCKET_NAME    
STATIC_URL = '/static/'
MEDIA_URL='http://your_s3_bucket.s3.amazonaws.com/%s/' % AWS_STORAGE_BUCKET_NAME    

# From: https://devcenter.heroku.com/articles/django-assets
# STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
MEDIAFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'


MEDIA_ROOT = os.path.join(ENV_PATH, '..', 'media/')
STATIC_ROOT = 'staticfiles'

STATICFILES_FINDERS = ('django.contrib.staticfiles.finders.FileSystemFinder',
                       'django.contrib.staticfiles.finders.AppDirectoriesFinder',
                       'dajaxice.finders.DajaxiceFinder')
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)



