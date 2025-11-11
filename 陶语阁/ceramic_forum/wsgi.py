import os
from django.core.wsgi import get_wsgi_application

# 设置 Django 环境变量（指定项目配置模块，必须与 settings.py 所在目录一致）
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ceramic_forum.settings')

# 获取 WSGI 应用实例，供 WSGI 服务器调用
application = get_wsgi_application()