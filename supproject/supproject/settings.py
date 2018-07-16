# coding:utf-8
"""
Django settings for supproject project.

Generated by 'django-admin startproject' using Django 1.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import json

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CONFIG_FILE = os.path.join(BASE_DIR, '.env')
CONFIG_INFO = {}
try:
    CONFIG = open(CONFIG_FILE).read()
    CONFIG = json.loads(CONFIG)
    CONFIG_INFO = CONFIG
except Exception as E:
    print('请用env文件', 'load .env error=%s' % E)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@5o@9)*g_!$yd41dvi+5rqh-1i^63_md1*_(56(f50%(@u@&)*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# 支持的项目和对应57数据库   57数据库采用sql语句脚本执行
DB_NAME = [
    {"p_id": 11, "db_name": "yh_yk_sx2","mark":""},
    {"p_id": 12, "db_name": "yh_yk_wl2","mark":""},
    {"p_id": 13, "db_name": "yh_yk_hx2","mark":""},
    {"p_id": 10, "db_name": "youhong_sx2zzcc","mark":""},
    {"p_id": 7, "db_name": "youhong_sx2py","mark":""},
    {"p_id": 8, "db_name": "youhong_sx2zzjx","mark":"zzjx_"},
    {"p_id": 9, "db_name": "youhong_sx3","mark":""},
    {"p_id": 2, "db_name": "youhong_px","mark":""},
]
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'models.gg',
    'models.siyou',
    'app',
    'vue'

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middleware.AuthenticationMiddleware',
]

ROOT_URLCONF = 'supproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'supproject.wsgi.application'

AUTH_PROFILE_MODULE = 'apps.account.Profile'
# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
DATABASE_ROUTERS = ['core.router.MyAppRouter']  # 同事连接多个数据库
DATABASES = {
    'siyou':{
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'youhong',
        'USER': CONFIG_INFO.get('YH_DB56_USER', ""),
        'PASSWORD': CONFIG_INFO.get('YH_DB56_PASSWORD', ""),
        'HOST': CONFIG_INFO.get('YH_DB56_HOST', ""),
        'PORT': CONFIG_INFO.get('YH_DB56_PORT', ""),
    },
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Etc/GMT-8'

USE_I18N = True

USE_L10N = True

USE_TZ = True

MEDIA_SITE = os.path.join(BASE_DIR, 'static/')
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
# # 静态文件路径
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)
