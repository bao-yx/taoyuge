from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-8xq&^%_7y9z@a#b$c*d(e)f+g-h=i_jk_lmno_pqrs'
# 注册应用
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 第三方应用
    'rest_framework',  # DRF框架
    'rest_framework_simplejwt',  # JWT认证

    # 自定义应用
    'forum',
]

AUTH_USER_MODEL = 'forum.User'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'taoyu_ge',
        'USER': 'root',
        'PASSWORD': 'wybyx1108.W',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
ROOT_URLCONF = 'ceramic_forum.urls'
WSGI_APPLICATION = 'ceramic_forum.wsgi.application'
# 配置DRF默认认证方式
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
# （可选）配置JWT令牌有效期
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),  # 访问令牌有效期1小时
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),  # 刷新令牌有效期7天
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # 1. 添加Session中间件（Admin依赖）
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    # 2. 添加认证中间件（Admin依赖）
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 3. 添加消息中间件（Admin依赖）
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
# 静态文件配置
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# 可选：部署时收集静态文件的目录（生产环境使用）
STATIC_ROOT = BASE_DIR / 'staticfiles'

# 语言设置为中文
LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

import os

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/community/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',  # Admin必需的模板引擎
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