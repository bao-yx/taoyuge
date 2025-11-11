from rest_framework import serializers
from .models import User, Post, Comment, Category, Tag, Like


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'avatar', 'bio', 'created_at']
        read_only_fields = ['id', 'created_at']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'parent', 'created_at']
        read_only_fields = ['id', 'created_at']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']


class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'author_username', 'content',
                  'parent', 'created_at', 'updated_at', 'likes_count']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']

    def get_likes_count(self, obj):
        return obj.likes.count()

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    category_name = serializers.ReadOnlyField(source='category.name')
    tags = TagSerializer(many=True, read_only=True)
    tags_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True, write_only=True, source='tags'
    )
    comments_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'author_username',
                  'category', 'category_name', 'tags', 'tags_ids',
                  'created_at', 'updated_at', 'views', 'comments_count',
                  'likes_count', 'is_featured']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at', 'views']

    def get_comments_count(self, obj):
        return obj.comments.count()

    def get_likes_count(self, obj):
        return obj.likes.count()

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'comment', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']

    def validate(self, data):
        # 确保只能点赞帖子或评论中的一个
        if not data.get('post') and not data.get('comment'):
            raise serializers.ValidationError("必须指定帖子或评论")
        if data.get('post') and data.get('comment'):
            raise serializers.ValidationError("只能点赞帖子或评论中的一个")
        return data

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
