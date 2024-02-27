from rest_framework import serializers
from .models import Category, Post, Comment

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    # Use SerializerMethodField to customize comments representation
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'

    def get_comments(self, post):
        # Filter and serialize only approved comments
        approved_comments = post.comments.filter(approved=True)
        serializer = CommentSerializer(approved_comments, many=True)
        return serializer.data