from .base import *


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '26d(ow7cz$(c_83cy1w%rg08&&mx&dozdh-4$)ad370*=sagkc'

ALLOWED_HOSTS = ['ec2-54-229-233-151.eu-west-1.compute.amazonaws.com']

SITE_ID = 1

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': '/etc/mysql/my.cnf',
        },
        'NAME': 'izzi_hotels',
        'USER': 'izzi',
        'PASSWORD': 'P455w0rd1'
    }
}

# Social Auth

SOCIAL_AUTH_FACEBOOK_KEY = '486369722261080'
SOCIAL_AUTH_FACEBOOK_SECRET = '5a7aa46f06e5b8b969c90c64bde2cef7'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '132557580705-hnbh4n4c0g7lqlfr94v1o0s1qt3jf348.apps.googleusercontent.com' 
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '3s_kg5xDuSezy6Pa6CEFccCf'

SOCIAL_AUTH_TWITTER_KEY = ''
SOCIAL_AUTH_TWITTER_SECRET = ''


# Google Maps
GOOGLE_MAPS_API_KEY = 'AIzaSyBvyGlW1sM-gDFqQtOcuBL09XyGsXXClm4'

# Media
MEDIA_ROOT = '/home/ubuntu/izzi-hotels-cms/'

# Emailing
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail.izzilifestylegroup.com'
EMAIL_USE_TLS = False
EMAIL_PORT = 587
EMAIL_HOST_USER = 'app@izzilifestylegroup.com'
EMAIL_HOST_PASSWORD = 'IzziIzzi123'


# Custom
FROM_EMAIL_ADDRESS = 'app@izzilifestylegroup.com'