from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Category, Tag, Post, Comment, Like

# 自定义用户管理（
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'is_active', 'date_joined')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('个人信息', {'fields': ('first_name', 'last_name', 'email')}),  # 移除自定义字段（若未定义）
        ('权限', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('日期', {'fields': ('last_login', 'date_joined')}),
    )
    readonly_fields = ('date_joined', 'last_login')

# 帖子管理
class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1
    fields = ('author', 'content', 'parent', 'created_at')
    readonly_fields = ('created_at',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'views', 'is_featured', 'created_at', 'image')
    list_filter = ('category', 'is_featured', 'created_at')
    search_fields = ('title', 'content')
    inlines = [CommentInline]
    fieldsets = (
        (None, {'fields': ('title', 'content', 'author', 'category', 'image')}),
        ('标签与状态', {'fields': ('tags', 'is_featured')}),
        ('统计', {'fields': ('views', 'created_at', 'updated_at')}),
    )
    readonly_fields = ('views', 'created_at', 'updated_at')

# 其他模型管理
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'created_at')
    search_fields = ('name', 'description')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'content', 'parent', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content', 'author__username', 'post__title')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'comment', 'created_at')
    list_filter = ('created_at',)

# 注册用户模型
admin.site.register(User, CustomUserAdmin)