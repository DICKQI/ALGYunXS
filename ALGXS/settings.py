"""
Django settings for ALGXS project.

Generated by 'django-admin startproject' using Django 2.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""
'''
ALGYun 1.0 
code XS
'''
import os
import pymysql

pymysql.install_as_MySQLdb()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'e@0+j9l3*z_h5t3!^iu1_0!d#6oxys9wx**mni9cq^+yzf9*yq'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'corsheaders',
    'django_summernote',

    'apps.account',
    'apps.market',
    'apps.PTJ',
    'apps.helps',
    'apps.FandQ',
    'apps.log',

]
# 富文本编辑器设置
SUMMERNOTE_CONFIG = {
    # Using SummernoteWidget - iframe mode
    'iframe': True,  # or set False to use SummernoteInplaceWidget - no iframe mode

    # Using Summernote Air-mode
    'airMode': False,

    # Use native HTML tags (`<b>`, `<i>`, ...) instead of style attributes
    'styleWithSpan': False,

    # Change editor size
    'width': '80%',
    'height': '480',

    # Use proper language setting automatically (default)
    'lang': 'zh-CN',

}
MIDDLEWARE = [
    # cors
    'corsheaders.middleware.CorsMiddleware',
    # alg middleware
    'ALGMiddleware.VisitLogMiddleware.VisitLogFirewall',
    'ALGMiddleware.IPFirewallMiddleware.IPFirewall',
    # 'ALGMiddleware.origin-allow.AllowOrigin',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

CORS_ALLOW_CREDENTIALS = True

CORS_ORIGIN_ALLOW_ALL = False

CORS_ORIGIN_WHITELIST = (

    'localhost:80',
    'localhost:443',
    'localhost:81',
    '127.0.0.1:8000',
    'localhost:8000'

)
CORS_ALLOW_METHODS = (

    'DELETE',

    'GET',

    'OPTIONS',

    'PATCH',

    'POST',

    'PUT',

    'VIEW',

)

CORS_ALLOW_HEADERS = (

    'accept',

    'XMLHttpRequest',

    'X_FILENAME',

    'accept-encoding',

    'authorization',

    'content-type',

    'dnt',

    'origin',

    'user-agent',

    'x-csrftoken',

    'x-requested-with',

    'Pragma',

    'X-Custom-Header',

)

ROOT_URLCONF = 'ALGXS.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'ALGXS.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ALGYunXS',
        'USER': 'root',
        'PASSWORD': 'macbook123456',
        'HOST': 'localhost',
        'PORT': 3306
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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

EMAIL_USE_SSL = True
EMAIL_HOST = 'smtp.163.com'  # 邮箱服务器
EMAIL_PORT = 994
EMAIL_HOST_USER = 'algyunxs@163.com'  # 帐号
EMAIL_HOST_PASSWORD = 'algyun666'  # 密码
EMAIL_FROM = 'algyun@163.com'

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

PAGE_NUM = 5  # 每页显示的文章数

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

SESSION_COOKIE_HTTPONLY = False

APPEND_SLASH = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static/")
# 配置静态文件目录
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'common_static'),
]
'''服务器端专用oss存储'''
ACCESS_KEY_ID = 'LTAIpK0JtS9hsWkG'
ACCESS_KEY_SECRET = 'cQpsrRs3Nhv6hTRpEMuUA2pjX6BlWs'
END_POINT = 'oss-cn-shenzhen-internal.aliyuncs.com'
BUCKET_NAME = 'algyunxs'
BUCKET_ACL_TYPE = 'public-read-write'
DEFAULT_FILE_STORAGE = 'aliyun_oss2_storage.backends.AliyunMediaStorage'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/').replace('\\', '/')
