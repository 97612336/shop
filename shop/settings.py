"""
Django settings for shop project.

Generated by 'django-admin startproject' using Django 2.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""
import json
import logging
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import requests

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '58#*pxz_j&*$g=8&vm9qhp%u0k191!!ni2yi^*0r-$hth0-1+l'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'shop.urls'

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

WSGI_APPLICATION = 'shop.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
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

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'


# api配置信息
def get_info():
    home_path = os.getenv('HOME')
    conf_path = os.path.join(home_path, 'conf')
    key_conf = os.path.join(conf_path, 'tkzs_conf')
    with open(key_conf, 'r') as f:
        res_text = f.read()
    info_dict = json.loads(res_text)
    return info_dict


TKZS_DICT = get_info()
APP_KEY = TKZS_DICT.get('appkey')
PASSWORD = TKZS_DICT.get('password')
MOBILE = TKZS_DICT.get('mobile')
PID = TKZS_DICT.get('pid')


# 获取登录后的session
def tk_session():
    session = requests.session()
    login_url = 'http://www.taokezhushou.com/login'
    login_data = {
        "mobile": MOBILE,
        "password": PASSWORD
    }
    login_res = session.post(login_url, data=login_data)
    logging.warning(login_res)
    logging.warning(MOBILE)
    logging.warning(PASSWORD)
    return session


# 模拟登陆后的session
TKZS_SESSION = tk_session()


def reset_tkzs_session(TKZS_SESSION):
    logging.warning(TKZS_SESSION)
    TKZS_SESSION = tk_session()
    print(TKZS_SESSION)
