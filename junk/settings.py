"""
Django settings for junk project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
_IN_PRODUCTION = True
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6+j3^26hw-$57#j&$+lqr1p1#)$v4rld=-6b(b#6je29uqkz=x'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'credentials',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)



ROOT_URLCONF = 'junk.urls'

WSGI_APPLICATION = 'junk.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases



if _IN_PRODUCTION == True:

	DATABASES = {
	   'default': {
		'ENGINE': 'django.db.backends.mysql',
		'HOST': '/cloudsql/myproject0922:cloud',
		'NAME': 'credentials',
		'USER': 'root',
	 
	    }
	}


else:
	DATABASES = {
	'default' : {
		'ENGINE': 'django.db.backends.mysql',
		'HOST': '173.194.83.40',
		#'HOST':'localhost',
		'NAME':'credentials',
		'USER':'root',
		'PASSWORD':'Guitar007',
	    }
	}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'


TEMPLATE_DIRS = (
	'templates',
)

# Django in memory upload maxed out at 6MB,No app engine storage ;(
FILE_UPLOAD_MAX_MEMORY_SIZE= 10000000


