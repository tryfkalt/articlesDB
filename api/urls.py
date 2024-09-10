from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register every viewset
router = DefaultRouter()
router.register(r'articles', views.ArticleViewSet)
router.register(r'tags', views.TagViewSet)
router.register(r'comments', views.CommentViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]