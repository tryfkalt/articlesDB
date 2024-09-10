from django.db import models
from django.contrib.auth.models import User
import uuid

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Article(models.Model):
    identifier = models.CharField(max_length=100, unique=True, default=uuid.uuid4) # Each article has a unique identifier
    title = models.CharField(max_length=255)
    abstract = models.TextField()
    publication_date = models.DateField(auto_now_add=True) # Automatically set the publication date when an article is created
    authors = models.ManyToManyField(User) # An article can have multiple authors
    tags = models.ManyToManyField(Tag, blank=True) # An article can have multiple tags

    def __str__(self): 
        return self.title
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # A comment is associated with a user. When a user is deleted, all comments by that user are deleted
    article = models.ForeignKey(Article, on_delete=models.CASCADE) # A comment is associated with an article. When an article is deleted, all comments on that article are deleted
    content  = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.article.title}'

