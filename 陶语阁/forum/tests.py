from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import User, Category, Post, Comment, Tag, Like


class ModelTests(TestCase):
    """测试数据模型的基本功能"""

    def setUp(self):
        """测试前的初始化：创建基础数据"""
        # 创建用户
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        # 创建分类
        self.category = Category.objects.create(
            name='陶瓷艺术',
            description='讨论陶瓷艺术相关内容'
        )
        # 创建帖子
        self.post = Post.objects.create(
            title='测试帖子',
            content='这是一篇测试帖子',
            author=self.user,
            category=self.category
        )
        # 创建标签
        self.tag = Tag.objects.create(name='测试标签')
        self.post.tags.add(self.tag)  # 关联标签


    def test_user_model(self):
        """测试用户模型的字符串表示和字段"""
        self.assertEqual(str(self.user), 'testuser')  # 验证 __str__ 方法
        self.assertEqual(self.user.email, 'test@example.com')  # 验证字段值


    def test_post_model(self):
        """测试帖子模型的功能"""
        self.assertEqual(str(self.post), '测试帖子')  # 验证 __str__ 方法
        self.assertEqual(self.post.author, self.user)  # 验证关联关系
        self.assertEqual(self.post.tags.count(), 1)  # 验证多对多关联
        self.assertEqual(self.post.views, 0)  # 初始浏览量为 0

        # 测试浏览量自增方法
        self.post.increment_views()
        self.post.refresh_from_db()  # 从数据库刷新数据
        self.assertEqual(self.post.views, 1)


    def test_like_model_unique_constraint(self):
        """测试点赞模型的唯一约束（同一用户不能重复点赞）"""
        # 第一次点赞（正常）
        Like.objects.create(user=self.user, post=self.post)
        # 第二次点赞同一帖子（应失败）
        with self.assertRaises(Exception):
            Like.objects.create(user=self.user, post=self.post)


class APITests(TestCase):
    """测试 API 接口的功能（使用 DRF 的 APIClient）"""

    def setUp(self):
        """初始化测试客户端和数据"""
        self.client = APIClient()  # DRF 测试客户端
        # 创建用户并登录
        self.user = User.objects.create_user(
            username='apitestuser',
            password='apipass123'
        )
        self.client.force_authenticate(user=self.user)  # 强制认证当前用户

        # 创建测试数据
        self.category = Category.objects.create(name='API测试分类')
        self.post = Post.objects.create(
            title='API测试帖子',
            content='API测试内容',
            author=self.user,
            category=self.category
        )


    def test_post_list_api(self):
        """测试帖子列表接口"""
        url = reverse('post-list')  # 假设帖子列表接口的路由名为 'post-list'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # 验证请求成功
        self.assertEqual(len(response.data), 1)  # 验证返回1条数据


    def test_create_post_api(self):
        """测试创建帖子接口"""
        url = reverse('post-list')
        data = {
            'title': '新测试帖子',
            'content': '新测试内容',
            'category': self.category.id,
            'tags_ids': []  # 空标签
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # 验证创建成功
        self.assertEqual(Post.objects.count(), 2)  # 验证数据库中新增1条记录
        self.assertEqual(response.data['author_username'], 'apitestuser')  # 验证作者正确


    def test_comment_create_api(self):
        """测试创建评论接口"""
        url = reverse('comment-list')  # 假设评论列表接口的路由名为 'comment-list'
        data = {
            'post': self.post.id,
            'content': '测试评论内容'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # 验证创建成功
        self.assertEqual(Comment.objects.count(), 1)  # 验证数据库中新增1条评论