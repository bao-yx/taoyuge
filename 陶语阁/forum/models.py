from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


# 扩展用户模型
class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True,verbose_name='头像')
    bio = models.TextField(max_length=500, blank=True, verbose_name='个人简历')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    # 陶瓷相关的兴趣领域
    ceramic_interests = models.ManyToManyField('Category', blank=True, related_name='interested_users')

    def __str__(self):
        return self.username


# 陶瓷分类
class Category(models.Model):
    name = models.CharField(max_length=100,verbose_name="分类名称",unique=True)
    description = models.TextField(blank=True,verbose_name="描述")
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='children')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "陶瓷分类"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 帖子模型
class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="标题")
    content = models.TextField( verbose_name="内容")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts',verbose_name="作者")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='posts',verbose_name="分类")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="发布时间")
    tags = models.ManyToManyField('Tag', blank=True, related_name='posts')
    created_at = models.DateTimeField(default=timezone.now, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    views = models.PositiveIntegerField(default=0, verbose_name="浏览量")
    like_count = models.PositiveIntegerField(default=0, verbose_name="点赞量")
    is_featured = models.BooleanField(default=False)
    image = models.ImageField(upload_to='post_images/', null=True, blank=True, verbose_name="图片")


    class Meta:
        verbose_name = "帖子"
        verbose_name_plural = "帖子"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def increment_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def sync_like_count(self):
        self.like_count = self.likes.count()
        self.save()


# 评论模型
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name="关联帖子")
    content = models.TextField(verbose_name="评论内容")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="评论作者")
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    created_at = models.DateTimeField(default=timezone.now, verbose_name="评论时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="评论更新时间")

    class Meta:
        verbose_name = "评论"
        verbose_name_plural = "评论"
        ordering = ['created_at']

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'


# 标签模型
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True,verbose_name="标签")

    class Meta:
        verbose_name = "标签"
        verbose_name_plural = "标签"

    def __str__(self):
        return self.name


# 点赞模型
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_likes', verbose_name="点赞用户")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes', null=True, blank=True,verbose_name="关联帖子")
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes', null=True, blank=True,verbose_name="评论")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="点赞时间")

    class Meta:
        verbose_name = "点赞"
        verbose_name_plural = "点赞"
        unique_together = [['user', 'post'], ['user', 'comment']]

    def __str__(self):
        if self.post:
            return f'{self.user.username} 点赞了《{self.post.title}》'
        return f'{self.user.username} 点赞了 {self.comment.author.username}的评论'
