import os
from django.core.asgi import get_asgi_application

# 设置Django环境变量（必须在获取ASGI应用前）
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ceramic_forum.settings')

# 获取Django的ASGI应用
application = get_asgi_application()
