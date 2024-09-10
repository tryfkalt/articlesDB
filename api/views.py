from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse,QueryDict
from django.utils.http import urlencode
from .models import Article, Comment, Tag
from .serializers import ArticleSerializer, CommentSerializer, TagSerializer
from .filters import ArticleFilter
from .permissions import IsAuthorOrReadOnly, IsCommentAuthorOrReadOnly
import csv


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all() 
    serializer_class = ArticleSerializer

    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly] # Custom permissions
    
    filter_backends = [DjangoFilterBackend] 
    filterset_class = ArticleFilter # Custom filters

    pagination_class = PageNumberPagination 
    
    def perform_create(self, serializer):
        authors = [self.request.user]  # Add the user who creates the article
        authors += serializer.validated_data.get('authors', [])  # Add the specified authors
        serializer.save(authors=authors)

    def list(self, request, *args, **kwargs):
        # Store the current filter parameters in the session
        request.session['article_filter_params'] = request.GET.urlencode() # urlencode method converts filter params to URL-encoded string
        print(request.session['article_filter_params'])
        return super().list(request, *args, **kwargs)

    @action(detail=False, methods=['get'])
    def export_csv(self, request):
        """
        Custom action to export filtered articles or specific articles by identifier as CSV.
        """
        if request.GET:
            query_params = request.GET
        else:
            # Retrieve the stored filter parameters from the session
            stored_params = request.session.get('article_filter_params', None)
            if stored_params:
                # Rebuild the query dict from the stored params
                query_params = QueryDict(stored_params)
            else:
                query_params = QueryDict()  # No filters applied
        # Get all articles as the initial queryset
        queryset = Article.objects.all()

        # Filter the articles based on the request parameters (GET parameters).
        articles = ArticleFilter(query_params, queryset=queryset).qs

        # Response object with content type set to 'text/csv'.
        response = HttpResponse(content_type='text/csv')
        
        # Set the content disposition header to trigger a file download.
        response['Content-Disposition'] = 'attachment; filename="articles.csv"'

        # Initialize a CSV writer object, which will write to the 'response' object.
        writer = csv.writer(response)

        # Write the header row to the CSV file, indicating column names.
        writer.writerow(['ID', 'Title', 'Abstract', 'Publication Date', 'Authors', 'Tags'])

        # Loop through the filtered articles and write each article's details as a row in the CSV file.
        for article in articles:
            # Get the authors of the article and join them into a comma-separated string.
            authors = ', '.join([author.username for author in article.authors.all()])

            # Get the tags of the article and join them into a comma-separated string.
            tags = ', '.join([tag.name for tag in article.tags.all()])
            
            # Write a row with article's ID, title, abstract, publication date, authors, and tags.
            writer.writerow([article.identifier, article.title, article.abstract, article.publication_date, authors, tags])
            
        return response

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsCommentAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
