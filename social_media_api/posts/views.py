from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User
from posts.models import Post, Comment
from .serializers import PostSerializer, CommentSerializer, UserSerializer

from rest_framework import filters
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


    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']  
    ordering_fields = ['created_at', 'updated_at']
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



class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def follow(self, request, pk=None):
        target_user = self.get_object()

        if target_user == request.user:
            return Response({"detail": "You cannot follow yourself."},status=status.HTTP_400_BAD_REQUEST)
        request.user.follow(target_user)
        return Response({"detail": f"You are now following {target_user.username}."},status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def unfollow(self, request, pk=None):
        target_user = self.get_object()

        if not request.user.is_following(target_user):
            return Response({"detail": "You are not following this user."},status=status.HTTP_400_BAD_REQUEST)
        request.user.unfollow(target_user)
        return Response({"detail": f"You have unfollowed {target_user.username}."},status=status.HTTP_200_OK)
