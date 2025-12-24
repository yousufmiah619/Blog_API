from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post, Like, Bookmark

class PostCreateUpdateSerializer(serializers.ModelSerializer):
    category_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'excerpt',
            'content',
            'featured_image',
            'read_time',
            'category_ids',
        ]

    def create(self, validated_data):
        category_ids = validated_data.pop('category_ids', [])
        post = Post.objects.create(**validated_data)
        if category_ids:
            post.categories.set(category_ids)
        return post

    def update(self, instance, validated_data):
        category_ids = validated_data.pop('category_ids', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if category_ids is not None:
            instance.categories.set(category_ids)

        return instance

User = get_user_model()

class AuthorSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'name', 'avatar']

    def get_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()

    def get_avatar(self, obj):
        profile = getattr(obj, 'profile', None)
        if profile and getattr(profile, 'avatar', None):
            return profile.avatar.url
        return "https://example.com/avatar.jpg"



class PostListSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_bookmarked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "excerpt",
            "featured_image",
            "author",
            "categories",
            "read_time",
            "created_at",
            "like_count",
            "comment_count",
            "is_liked",
            "is_bookmarked",
        ]

    def get_author(self, obj):
        return {
            "id": obj.author.id,
            "name": obj.author.username,
            "avatar": None   # future ready
        }

    def get_categories(self, obj):
        return [cat.name for cat in obj.categories.all()]

    def get_like_count(self, obj):
        return obj.likes.count()

    def get_comment_count(self, obj):
        return obj.comments.count()

    def get_is_liked(self, obj):
        user = self.context["request"].user
        if user.is_anonymous:
            return False
        return obj.likes.filter(user=user).exists()

    def get_is_bookmarked(self, obj):
        user = self.context["request"].user
        if user.is_anonymous:
            return False
        return obj.bookmarks.filter(user=user).exists()
