import os
gettext = lambda s: s
DATA_DIR = os.path.dirname(os.path.dirname(__file__))

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CSV_DIR = os.path.join(BASE_DIR, "csv")

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'e^l@vth%)g49j=_!7w%k3uomieqpemokyta18yj2$ay81dk^u&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['www.wenyenchi.com', 'localhost']

# Application definition

ROOT_URLCONF = 'tap_site.urls'

WSGI_APPLICATION = 'tap_site.wsgi.application'

LANGUAGE_CODE = 'en'

TIME_ZONE = 'Africa/Nairobi'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(DATA_DIR, 'media')
STATIC_ROOT = os.path.join(DATA_DIR, 'static')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'tap_site', 'static'),
)
SITE_ID = 1


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'tap_site', 'templates'),],
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.template.context_processors.csrf',
                'django.template.context_processors.tz',
                'sekizai.context_processors.sekizai',
                'django.template.context_processors.static',
                'postman.context_processors.inbox',
                'cms.context_processors.cms_settings'
            ],
            'loaders': [
                'admin_tools.template_loaders.Loader',
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
                'django.template.loaders.eggs.Loader',

            ],
        },
    },
]


MIDDLEWARE_CLASSES = (
    'raven.contrib.django.raven_compat.middleware.Sentry404CatchMiddleware',
    'cms.middleware.utils.ApphookReloadMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'pagination.middleware.PaginationMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware'
)

#Site Protection
CSRF_COOKIE_SECURE = True 
#SESSION_COOKIE_SECURE = True
X_FRAME_OPTIONS = 'DENY'
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
#SECURE_HSTS_PRELOAD = True
#SECURE_HSTS_SECONDS = 3600
#SECURE_REDIRECT_EXEMPT
#SECURE_SSL_HOST = True
#SECURE_SSL_REDIRECT = True

INSTALLED_APPS = (
    'djangocms_admin_style',
    'colorfield',
    'fluent_dashboard',
    # enable the admin
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',
    'admin_timeline',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'django.contrib.humanize',
    'django.contrib.postgres',
    'raven.contrib.django.raven_compat',
    'cms',
    'menus',
    'sekizai',
    'treebeard',
    'djangocms_text_ckeditor',
    'filer',
    'easy_thumbnails',
    #'djangocms_column',
    'djangocms_link',
    'cmsplugin_filer_file',
    'cmsplugin_filer_folder',
    'cmsplugin_filer_image',
    'cmsplugin_filer_utils',
    'djangocms_style',
    'djangocms_snippet',
    'djangocms_googlemap',
    'djangocms_video',
    'debug_toolbar',
    'tap_site',
    'survey',
    'bootstrapform',
    'bootstrap3',
    'polls',
    'reviews',
    'counties',
    'companies',
    'colleges',
    'constituencies',
    'wards',
    'hospitals',
    'hotels',
    'schools',
    'sports',
    'parks',
    'associations',
    'sorl.thumbnail',
    'markdown_deux',
    'helpdesk',
    'postman',
    'pinax.notifications',
    'mailer',
    'ajax_select',
    'crispy_forms',
    'widget_tweaks',
    'contact_form',
    'mptt',
    'sklearn',
    'ads',
    'django_comments_xtd',
    'django_comments',
    'django_social_share',
    'analytical',
   
  


    
)

LANGUAGES = (
    ## Customize this
    ('en', gettext('en')),
    ('fr', gettext('fr')),
    ('de', gettext('de')),
    ('sw', gettext('sw')),
)

CMS_LANGUAGES = {
    ## Customize this
    1: [
        {
            'name': gettext('en'),
            'code': 'en',
            'redirect_on_fallback': True,
            'public': True,
            'hide_untranslated': False,
        },
    ],
    'default': {
        'redirect_on_fallback': True,
        'public': True,
        'hide_untranslated': False,
    },
}

CMS_TEMPLATES = (
    ## Customize this
    ('fullwidth.html', 'Fullwidth'),
    ('sidebar_left.html', 'Sidebar Left'),
    ('sidebar_right.html', 'Sidebar Right'),
    ('terms.html', 'Terms'),
    ('privacy.html', 'Privacy'),
)

TEMPLATE_STRING_IF_INVALID = ""
CMS_PERMISSION = True

CMS_PLACEHOLDER_CONF = {}

DATABASES = {
    'default': {
        'CONN_MAX_AGE': 0,
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': 'localhost',
        'NAME': 'tap_master',
        'PASSWORD': 'tap2017',
        'PORT': '5432',
        'USER': 'postgres'
    }
}

MIGRATION_MODULES = {
    
}

THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters'
)

#registration settings
ACCOUNT_ACTIVATION_DAYS = 7 # One-week activation window;
REGISTRATION_AUTO_LOGIN = True # Automatically log the user in.
LOGIN_URL = 'accounts/login'
LOGIN_REDIRECT_URL = "/en/"

#email backend settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # Django mailer
MAILER_EMAIL_MAX_BATCH = None #integer or None control;how many emails are sent successfully before stopping the current run
MAILER_EMAIL_MAX_DEFERRED = None  # integer or None;after how many failed/deferred emails should it stop
MAILER_EMAIL_THROTTLE = 0  # passed to time.sleep();how much time to wait between each email
EMAIL_HOST = "smtp.mail.com"
EMAIL_PORT = "587"
EMAIL_HOST_USER = "admin"
EMAIL_HOST_PASSWORD = "yourpassword"
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = "Helpdesk <helpdesk@wenyenchi.com>"
EMAIL_USE_LOCALTIME = True
EMAIL_USE_TLS = True
EMAIL_SUBJECT_PREFIX = '[Wenyenchi.com] '

#cache settings
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cache_table',
    }
}
#fluent dashboard
ADMIN_TOOLS_INDEX_DASHBOARD = 'fluent_dashboard.dashboard.FluentIndexDashboard'
ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'fluent_dashboard.dashboard.FluentAppIndexDashboard'
ADMIN_TOOLS_MENU = 'fluent_dashboard.menu.FluentMenu'

#survey settings
USER_DID_NOT_ANSWER = "Left blank"
TEX_CONFIGURATION_FILE = os.path.join(BASE_DIR, "doc", "example_conf.yaml")
SURVEY_DEFAULT_PIE_COLOR = "red!50"

#comments extended
COMMENTS_APP = 'django_comments_xtd'
#  To help obfuscating comments before they are sent for confirmation.
COMMENTS_XTD_SALT = (b"Timendi causa est nescire. "
                     b"Aequam memento rebus in arduis servare mentem.")

# Source mail address used for notifications.
COMMENTS_XTD_FROM_EMAIL = "helpdesk@wenyenchi.com"

# Contact mail address to show in messages.
COMMENTS_XTD_CONTACT_EMAIL = "helpdesk@wenyenchi.com"
COMMENTS_XTD_MAX_THREAD_LEVEL = 2
#COMMENTS_XTD_LIST_ORDER = ('-thread_id', 'order')  # default is ('thread_id', 'order')
# COMMENTS_XTD_APP_MODEL_OPTIONS = {
#     'default': {
#         'allow_flagging': True,
#         'allow_feedback': True,
#         'show_feedback': True,
#     }
# }

CONTENT_TYPES = ['image']
# 2.5MB - 2621440
# 5MB - 5242880
# 10MB - 10485760
# 20MB - 20971520
# 50MB - 5242880
# 100MB - 104857600
# 250MB - 214958080
# 500MB - 429916160
MAX_UPLOAD_SIZE = 2621440

FILE_UPLOAD_MAX_MEMORY_SIZE = 2621440

GOOGLE_MAPS_API_KEY ='AIzaSyAug2LPZSdT1s9yM3adeFtyG65WeVNqFS0'


#Notification Settings
PINAX_NOTIFICATION_BACKENDS = [
    ("email", "pinax.notifications.backends.email.EmailBackend"),
]
PINAX_NOTIFICATIONS_QUEUE_ALL = False
PINAX_NOTIFICATIONS_LOCK_WAIT_TIMEOUT = -1

#channels settings

redis_host = os.environ.get('REDIS_HOST', 'localhost')

# Channel layer definitions
# http://channels.readthedocs.org/en/latest/deploying.html#setting-up-a-channel-backend
CHANNEL_LAYERS = {
    "default": {
        # This example app uses the Redis channel layer implementation asgi_redis
        "BACKEND": "asgi_redis.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(redis_host, 6379)],
        },
       "ROUTING": "tap_site.routing.channel_routing", # We will create it in a moment
    },
}


#django-postman settings
POSTMAN_I18N_URLS = True  # default is False
POSTMAN_DISALLOW_ANONYMOUS = True  # default is False
POSTMAN_DISALLOW_MULTIRECIPIENTS = True  # default is False
POSTMAN_DISALLOW_COPIES_ON_REPLY = True  # default is False
POSTMAN_DISABLE_USER_EMAILING = True  # default is False
POSTMAN_FROM_EMAIL = 'from@host.tld'  # default is DEFAULT_FROM_EMAIL
POSTMAN_PARAMS_EMAIL = None  # default is None
POSTMAN_AUTO_MODERATE_AS = True  # default is None
POSTMAN_SHOW_USER_AS = 'get_full_name'  # default is None
POSTMAN_NAME_USER_AS = 'last_name'  # default is None
POSTMAN_QUICKREPLY_QUOTE_BODY = True  # default is False
POSTMAN_NOTIFIER_APP = None  # default is 'notification'
POSTMAN_MAILER_APP = None  # default is 'mailer'
# POSTMAN_AUTOCOMPLETER_APP = {
    # 'name': '',  # default is 'ajax_select'
    # 'field': '',  # default is 'AutoCompleteField'
    # 'arg_name': '',  # default is 'channel'
    # 'arg_default': 'postman_friends',  # no default, mandatory to enable the feature
# }  # default is

#Django ADS settings
ADS_GOOGLE_ADSENSE_CLIENT = 'ca-pub-xxxxxxxxxxxxxxxx'  # OPTIONAL - DEFAULT TO None

ADS_ZONES = {
    'header': {
        'name': ('Header'),
        'ad_size': {
            'xs': '720x150',
            'sm': '800x90',
            'md': '800x90',
            'lg': '800x90'
        },
        'google_adsense_slot': 'xxxxxxxxx',  # OPTIONAL - DEFAULT TO None
        'google_adsense_format': 'auto',  # OPTIONAL - DEFAULT TO None
    },
    'content': {
        'name': ('Content'),
        'ad_size': {
            'xs': '720x150',
            'sm': '800x90',
            'md': '800x90',
            'lg': '800x90'
        },
        'google_adsense_slot': 'xxxxxxxxx',  # OPTIONAL - DEFAULT TO None
        'google_adsense_format': 'auto',  # OPTIONAL - DEFAULT TO None
    },
    'sidebar': {
        'name': ('Sidebar'),
        'ad_size': {
            'xs': '720x150',
            'sm': '800x90',
            'md': '800x90',
            'lg': '800x90'
        },
        'google_adsense_slot': 'xxxxxxxxx',  # OPTIONAL - DEFAULT TO None
        'google_adsense_format': 'auto',  # OPTIONAL - DEFAULT TO None
    },
}

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


#Logging

import raven

RAVEN_CONFIG = {
    'dsn': 'https://<key>:<secret>@sentry.io/<project>',
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'ERROR', # To capture more than ERROR, change to WARNING, INFO, etc.
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            'tags': {'custom-tag': 'x'},
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}

#debug toolbar
INTERNAL_IPS = '127.0.0.1'

#django analytical
GOOGLE_ANALYTICS_PROPERTY_ID = 'UA-1234567-8'
PIWIK_DOMAIN_PATH = 'your.piwik.server/optional/path'
PIWIK_SITE_ID = '123'
YANDEX_METRICA_COUNTER_ID = '12345678'