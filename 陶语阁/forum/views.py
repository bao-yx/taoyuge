from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import User, Post, Comment, Category, Tag, Like
from .serializers import (
    UserSerializer, PostSerializer, CommentSerializer,
    CategorySerializer, TagSerializer, LikeSerializer
)
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .forms import LoginForm,RegisterForm,PostForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import os



# 注册视图
def user_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('forum_index')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


# 登录视图
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('forum_index')  # 登录后跳转到首页
    else:
        form = LoginForm()  # GET 请求显示空表单
    return render(request, 'login.html', {'form': form})

# 登出视图
def user_logout(request):
    logout(request)
    return redirect('home')  # 登出后跳转到首页



# 论坛首页视图
@login_required(login_url='/login/')
def forum_index(request):
    categories = Category.objects.all()
    posts = Post.objects.all().order_by('-created_at')
    return render(request, "html/community.html", {
        "posts": posts,
        "categories": categories,
    })

# 帖子详情视图
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.views += 1
    post.save()
    return render(request, "forum/post_detail.html", {"post": post})

# 分类帖子列表视图
def category_posts(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    posts = Post.objects.filter(category=category).order_by('-created_at')
    return render(request, "forum/category.html", {"category": category, "posts": posts})





class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    只允许作者修改自己的内容
    """

    def has_object_permission(self, request, view, obj):
        # 读权限允许任何请求
        if request.method in permissions.SAFE_METHODS:
            return True
        # 写权限只允许作者
        return obj.author == request.user


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    用户信息API
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email']

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        """获取当前登录用户信息"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    陶瓷分类API
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']


class TagViewSet(viewsets.ModelViewSet):
    """
    标签API
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class PostViewSet(viewsets.ModelViewSet):
    """
    帖子API
    """
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'tags', 'author']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'views', 'likes_count']

    @action(detail=True, methods=['get'])
    def increment_view(self, request, pk=None):
        """增加帖子浏览量"""
        post = self.get_object()
        post.increment_views()
        return Response({'status': 'view count increased'})

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        """点赞帖子"""
        post = self.get_object()
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if created:
            post.sync_like_count()
            return Response({
                'status': 'post liked',
                'is_liked': True,
                'like_count': post.like_count
            }, status=status.HTTP_201_CREATED)
        return Response({
            'status': 'already liked',
            'is_liked': True,
            'like_count': post.like_count
        }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def unlike(self, request, pk=None):
        """取消点赞帖子"""
        post = self.get_object()
        try:
            like = Like.objects.get(user=request.user, post=post)
            like.delete()
            post.sync_like_count()
            return Response({
                'status': 'like removed',
                'is_liked': False,
                'like_count': post.like_count
            })
        except Like.DoesNotExist:
            return Response({
                'status': 'not liked',
                'is_liked': False,
                'like_count': post.like_count
            }, status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(viewsets.ModelViewSet):
    """
    评论API
    """
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['post', 'author', 'parent']

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        """点赞评论"""
        comment = self.get_object()
        like, created = Like.objects.get_or_create(user=request.user, comment=comment)
        if created:
            return Response({'status': 'comment liked'}, status=status.HTTP_201_CREATED)
        return Response({'status': 'already liked'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def unlike(self, request, pk=None):
        """取消点赞评论"""
        comment = self.get_object()
        try:
            like = Like.objects.get(user=request.user, comment=comment)
            like.delete()
            return Response({'status': 'like removed'})
        except Like.DoesNotExist:
            return Response({'status': 'not liked'}, status=status.HTTP_400_BAD_REQUEST)

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)  # 若支持图片上传，需传入request.FILES
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # 关联当前登录用户
            post.save()
            return redirect('post_detail', post.pk)  # 跳转到帖子详情页
    else:
        form = PostForm()
    return render(request, 'forum/create_post.html', {'form': form})


@login_required
def post_like(request, post_id):
    if request.method != 'POST':
        return JsonResponse({'error': '仅支持POST请求'}, status=405)

    post = get_object_or_404(Post, id=post_id)
    user = request.user
    like, created = Like.objects.get_or_create(user=user, post=post)

    if created:
        post.like_count += 1
    else:
        like.delete()
        post.like_count -= 1
    post.save()

    return JsonResponse({
        'success': True,
        'is_liked': created,
        'like_count': post.like_count
    })


@login_required
def add_comment(request, post_id):
    """处理帖子评论提交"""
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            Comment.objects.create(
                post=post,
                author=request.user,
                content=content
            )
    return redirect('post_detail', pk=post_id)



@login_required(login_url='/login/')
def my_profile(request):
    user = request.user
    my_posts = Post.objects.filter(author=user).order_by('-created_at')
    liked_posts = Post.objects.filter(post_likes__user=user).order_by('-post_likes__created_at')

    context = {
        'user': user,
        'my_posts': my_posts,
        'liked_posts': liked_posts
    }
    return render(request, 'forum/my_profile.html', context)


@login_required
def edit_profile(request):
    """编辑个人信息"""
    if request.method == 'POST':
        # 处理表单提交（头像、简介等）
        user = request.user
        user.bio = request.POST.get('bio', '')
        if 'avatar' in request.FILES:
            user.avatar = request.FILES['avatar']
        user.save()
        return redirect('my_profile')

    # GET请求：展示编辑表单
    return render(request, 'forum/edit_profile.html', {'user': request.user})



@login_required
def delete_post(request, post_id):
    """删除帖子（仅作者或管理员可操作）"""
    post = get_object_or_404(Post, id=post_id)

    # 权限验证：只有帖子作者或管理员能删除
    if request.user != post.author and not request.user.is_staff:
        messages.error(request, "你没有权限删除这篇帖子！")
        return redirect('post_detail', post_id=post.id)

    # 执行删除
    post.delete()
    messages.success(request, "帖子已成功删除！")
    return redirect('my_profile')


# 编辑帖子
@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            edited_post = form.save(commit=False)

            # 关键：如果上传了新图片，删除原有图片文件
            if 'image' in request.FILES:
                # 检查原有图片是否存在，存在则删除
                if edited_post.image and os.path.exists(edited_post.image.path):
                    os.remove(edited_post.image.path)

            # 保存新图片和帖子信息
            edited_post.save()
            form.save_m2m()  # 保存多对多字段（如tags）
            return redirect('my_profile')  # 跳转回个人主页，刷新后查看效果
    else:
        form = PostForm(instance=post)

    return render(request, 'forum/edit_post.html', {
        'form': form,
        'post': post
    })


#动态路由
def dynasty_detail(request, name):
    template_name = f'html/{name}.html'
    return render(request, template_name)

