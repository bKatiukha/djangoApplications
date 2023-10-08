from rest_framework import serializers

from src.blog.models import Category, Post


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CategoryWithCountSerializer(serializers.ModelSerializer):
    published_post_count = serializers.IntegerField(default=0)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'published_post_count']


class PostSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Post
        fields = '__all__'


class CreatePostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['title', 'slug', 'photo', 'content', 'is_published', 'category']
