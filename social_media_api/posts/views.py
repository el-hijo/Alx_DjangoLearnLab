from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied

from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer

# Create your views here.

class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
    
        post_id = self.request.data.get("post")

        if not post_id:
            raise PermissionDenied("Post ID is required to create a comment.")

        serializer.save(author=self.request.user,post_id=post_id)
