import django_filters
from .models import Article, Tag, Comment
from django.contrib.auth.models import User

class ArticleFilter(django_filters.FilterSet):
    year = django_filters.NumberFilter(field_name='publication_date', lookup_expr='year') # Filter by year

    month = django_filters.NumberFilter(field_name='publication_date', lookup_expr='month') # Filter by month

    authors = django_filters.ModelMultipleChoiceFilter(
        field_name='authors',
        queryset=User.objects.all()
    ) # Filter by authors

    tags = django_filters.ModelMultipleChoiceFilter(
        field_name='tags',
        queryset=Tag.objects.all()
    ) # Filter by tags

    keywords = django_filters.CharFilter(method='filter_by_keyword', label='Keyword Search') # Filter by keyword

    class Meta:
        model = Article
        fields = ['year', 'month', 'authors', 'tags', 'keywords']

    def filter_by_keyword(self, queryset, name, value): # Custom filter method
        return queryset.filter(title__icontains=value) | queryset.filter(abstract__icontains=value)