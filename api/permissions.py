from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

class IsAuthorOrReadOnly(BasePermission):
    """
    Custom permission to only allow authors of an article to edit or delete it.
    """
    def has_object_permission(self, request, view, obj):
        # Allow read-ony permissions for any request
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        # Write permissions are only allowed if the user is one of the authors
        if request.user in obj.authors.all():
            return True
        
        # If not one of the authors, raise permission denied
        raise PermissionDenied("You are not allowed to modify this article.")

class IsCommentAuthorOrReadOnly(BasePermission):
    """
    Custom permission to only allow writers of a comment to edit or delete it.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        if request.user == obj.user:
            return True
        
        raise PermissionDenied("You are not allowed to modify this comment.")