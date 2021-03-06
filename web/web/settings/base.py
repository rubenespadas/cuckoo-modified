# Copyright (C) 2010-2015 Cuckoo Foundation.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

import sys
from unipath import Path

# Cuckoo path.
BASE_DIR = Path(__file__).ancestor(3)
SETTINGS_DIR = Path(__file__).ancestor(1)
CUCKOO_PATH = Path(__file__).ancestor(4)
sys.path.append(CUCKOO_PATH)

from lib.cuckoo.common.config import Config

cfg = Config("reporting")

# Error handling for database backends
if not cfg.mongodb.get("enabled") and not cfg.elasticsearchdb.get("enabled"):
    raise Exception("No database backend reporting module is enabled! Please enabled ElasticSearch or MongoDB.")

if cfg.mongodb.get("enabled") and cfg.elasticsearchdb.get("enabled"):
    raise Exception("Both database backend reporting modules are enabled. Please only enabled ElasticSearch or MongoDB.")

# Get connection options from reporting.conf.
MONGO_HOST = cfg.mongodb.get("host", "127.0.0.1")
MONGO_PORT = cfg.mongodb.get("port", 27017)
MONGO_DB = cfg.mongodb.get("db", "cuckoo")

ELASTIC_HOST = cfg.elasticsearchdb.get("host", "127.0.0.1")
ELASTIC_PORT = cfg.elasticsearchdb.get("port", 9200)
ELASTIC_INDEX = cfg.elasticsearchdb.get("index", "cuckoo")

moloch_cfg = Config("reporting").moloch
aux_cfg =  Config("auxiliary")
vtdl_cfg = Config("auxiliary").virustotaldl

MOLOCH_BASE = moloch_cfg.get("base", None)
MOLOCH_NODE = moloch_cfg.get("node", None)
MOLOCH_ENABLED = moloch_cfg.get("enabled", False)

GATEWAYS = aux_cfg.get("gateways")
VTDL_ENABLED = vtdl_cfg.get("enabled",False)
VTDL_PRIV_KEY = vtdl_cfg.get("dlprivkey",None)
VTDL_INTEL_KEY = vtdl_cfg.get("dlintelkey",None)
VTDL_PATH = vtdl_cfg.get("dlpath",None)

# Enabled/Disable Zer0m0n tickbox on the submission page
OPT_ZER0M0N = False

# To disable comment support, change the below to False
COMMENTS = True

DEBUG = False

# Database settings. We don't need it.
DATABASES = {}

SITE_ID = 1

LANGUAGE_CODE = "en-us"

MAX_UPLOAD_SIZE = 26214400

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# Disabling time zone support and using local time for web interface and storage.
# See: https://docs.djangoproject.com/en/1.5/ref/settings/#time-zone
USE_TZ = False
TIME_ZONE = None

# Unique secret key generator.
# Secret key will be placed in secret_key.py file.
try:
    from secret_key import *
except ImportError:
    from django.utils.crypto import get_random_string
    key = get_random_string(50, "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)")

    # Write secret_key.py
    with open(SETTINGS_DIR.child("secret_key.py"), "w") as key_file:
        key_file.write("SECRET_KEY = \"{0}\"".format(key))

    # Reload key.
    from secret_key import *

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR.child('static'),
]

STATIC_ROOT = BASE_DIR.child('collected_statics')

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Cuckoo headers.
    'web.headers.CuckooHeaders',
    'ratelimit.middleware.RatelimitMiddleware',
)

ROOT_URLCONF = 'web.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'web.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR.child('templates'),
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
    },
]


RATELIMIT_VIEW = 'api.views.limit_exceeded'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    #'django.contrib.sites',
    #'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'analysis',
    'compare',
    'api',
    'ratelimit',
)

LOGIN_REDIRECT_URL = "/"

# Fix to avoid migration warning in django 1.7 about test runner (1_6.W001).
# In future it could be removed: https://code.djangoproject.com/ticket/23469
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
