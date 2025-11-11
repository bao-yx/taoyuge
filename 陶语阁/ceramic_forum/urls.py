from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from forum import views
from rest_framework.routers import DefaultRouter
from forum.views import PostViewSet


router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')

urlpatterns = [



    path('admin/', admin.site.urls),
    path('api/', include('forum.urls')),  # 引入forum应用的URL
    path('', include('forum.urls')),  # 包含 forum 应用的路由
    path('community/', views.forum_index, name='forum_community'),
    path('api/', include(router.urls)),
    
]

# 开发环境下，添加媒体文件的静态路由（生产环境需用Nginx等配置）
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)