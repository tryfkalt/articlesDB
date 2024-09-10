from rest_framework import serializers
from .models import Article, Comment, Tag
from django.contrib.auth.models import User

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name'] # Return the ID and name of the tag

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']  # Return the ID, username, email, first name, and last name of the user

class ArticleSerializer(serializers.ModelSerializer):
    # authors = UserSerializer(many=True)
    authors = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all()) 
    # tags = TagSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())

    class Meta:
        model = Article
        fields = ['id', 'title', 'abstract', 'publication_date', 'authors', 'tags']
    def to_representation(self, instance):
        """ Override to return detailed user info for authors on read requests"""
        response = super().to_representation(instance)
        response['authors'] = UserSerializer(instance.authors, many=True).data
        response['tags'] = TagSerializer(instance.tags, many=True).data
        return response

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    article = serializers.PrimaryKeyRelatedField(queryset=Article.objects.all())

    class Meta:
        model = Comment
        fields = ['id', 'user', 'article', 'content', 'created_at', 'updated_at']
