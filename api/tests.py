from django.test import TestCase
from django.contrib.auth.models import User
from .models import Article, Tag, Comment
from .views import ArticleViewSet, TagViewSet, CommentViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsAuthorOrReadOnly, IsCommentAuthorOrReadOnly

class TestModels(TestCase):
    def setUp(self):
        """
        Setup before each test
        """
        self.author = User.objects.create(username='Test User', password='Test Password')
        self.tag = Tag.objects.create(name='Test Tag')

    def test_model_article(self):
        
        article_item = Article.objects.create(title='Test Article', abstract='Test Abstract')
        article_item.authors.add(self.author)
        article_item.tags.add(self.tag)
        article_item.save()
        self.assertEqual(str(article_item), 'Test Article')
        self.assertTrue(isinstance(article_item, Article))

    def test_model_tag(self):
        Tag.objects.filter(name='Test Tag').delete()  # Ensure no duplicate tags
        tag_item = Tag.objects.create(name='Test Tag')
        self.assertEqual(str(tag_item), 'Test Tag')
        self.assertTrue(isinstance(tag_item, Tag))

    def test_model_comment(self):
        article_item = Article.objects.create(title='Test Article', abstract='Test Abstract')
        article_item.authors.add(self.author)
        article_item.tags.add(self.tag)
        article_item.save()
        print(article_item)
        comment_item = Comment.objects.create(user=self.author, article=article_item, content='Test Content')
        self.assertEqual(str(comment_item), 'Comment by Test User on Test Article')
        self.assertTrue(isinstance(comment_item, Comment))

class TestViewSet(TestCase):
    def setUp(self):
        """
        Setup before each test
        """
        self.author = User.objects.create(username='Test User', password='Test Password')
        self.tag = Tag.objects.create(name='Test Tag')
        self.article = Article.objects.create(title='Test Article', abstract='Test Abstract')
        self.article.authors.add(self.author)
        self.article.tags.add(self.tag)
        self.article.save()
        self.comment = Comment.objects.create(user=self.author, article=self.article, content='Test Content')

    def test_viewset_article(self):
        viewset = ArticleViewSet()
        self.assertEqual(viewset.queryset.count(), 1)
        self.assertEqual(viewset.serializer_class.Meta.model, Article)
        self.assertEqual(viewset.permission_classes, [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly])

    def test_viewset_tag(self):
        viewset = TagViewSet()
        self.assertEqual(viewset.queryset.count(), 1)
        self.assertEqual(viewset.serializer_class.Meta.model, Tag)
        self.assertEqual(viewset.permission_classes, [IsAuthenticatedOrReadOnly])

    def test_viewset_comment(self):
        viewset = CommentViewSet()
        self.assertEqual(viewset.queryset.count(), 1)
        self.assertEqual(viewset.serializer_class.Meta.model, Comment)
        self.assertEqual(viewset.permission_classes, [IsAuthenticatedOrReadOnly, IsCommentAuthorOrReadOnly])

    
