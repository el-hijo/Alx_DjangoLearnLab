from rest_framework import viewsets, generics, permissions, status,filters
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer, UserSerializer
from notifications.models import Notification
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

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
        post = Post.objects.get(pk=post_id)
        serializer.save(author=self.request.user, post_id=post_id)
        if not post_id:
            raise PermissionDenied("Post ID is required to create a comment.")

        serializer.save(author=self.request.user,post_id=post_id)

        Notification.objects.create(recipient=post.author,actor=self.request.user,verb="commented on your post",target=post,)



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


class UserFeedView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer

    def get(self, request):
        following_users = request.user.following.all()
        posts = Post.objects.filter(author__in=following_users).order_by("-created_at")

        serializer = self.serializer_class(posts, many=True)
        return Response(serializer.data)
    
class LikePostView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if not created:
            return Response({"detail": "You have already liked this post."},status=status.HTTP_400_BAD_REQUEST)
        Notification.objects.create(recipient=post.author,actor=request.user,verb="liked your post",target=post,)
        return Response({"detail": "Post liked successfully."}, status=status.HTTP_201_CREATED)

        Notification.objects.create(recipient=post.author,actor=request.user,verb="liked your post",target=post,)



class UnlikePostView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)
        like = Like.objects.filter(user=request.user, post=post).first()

        if not like:
            return Response(
                {"detail": "You have not liked this post."},status=status.HTTP_400_BAD_REQUEST)

        like.delete()

        return Response({"detail": "Like removed successfully."}, status=status.HTTP_200_OK)
