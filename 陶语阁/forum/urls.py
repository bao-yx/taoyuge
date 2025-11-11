from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    UserViewSet, PostViewSet, CommentViewSet,
    CategoryViewSet, TagViewSet
)
from . import views
from django.views.generic import TemplateView

# API路由配置
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'tags', TagViewSet)

urlpatterns = [
    # API路由
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api-auth/', include('rest_framework.urls')),

    # 静态路由
    path('', TemplateView.as_view(template_name='html/home.html'), name='home'),
    path('culture/', TemplateView.as_view(template_name='html/culture.html'), name='culture_page'),
    path('technical/', TemplateView.as_view(template_name='html/technical.html'), name='technical_page'),
    path('picture/', TemplateView.as_view(template_name='html/picture.html'), name='picture_page'),

    #动态路由
    path('dynasty/<str:name>/', views.dynasty_detail, name='dynasty_detail'),
    path('culture/', TemplateView.as_view(template_name='html/culture.html'), name='culture'),

    # 认证相关路由
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # 论坛功能路由
    path('community/', views.forum_index, name='forum_index'),
    path('forum/post/<int:pk>/', views.post_detail, name='post_detail'),
    path('forum/category/<int:category_id>/', views.category_posts, name='category_posts'),
    path('forum/create/', views.create_post, name='create_post'),
    path('forum/post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('my/profile/', views.my_profile, name='my_profile'),
    path('my/profile/edit/', views.edit_profile, name='edit_profile'),
    path('forum/post/<int:post_id>/edit/', views.edit_post, name='edit_post'),
    path('forum/post/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('forum/post/<int:post_id>/like/', views.post_like, name='post_like'),
]
