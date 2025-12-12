from rest_framework import generics, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User as CustomUser

from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from notifications.models import Notification

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()     
    serializer_class = RegisterSerializer


class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            "token": token.key,
            "user_id": user.id,
            "username": user.username
        })


class FollowUserView(generics.GenericAPIView):
    queryset = CustomUser.objects.all()     
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def post(self, request, user_id):
        try:
            target_user = CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return Response({"detail": "User not found."},
                            status=status.HTTP_404_NOT_FOUND)

        if target_user == request.user:
            return Response({"detail": "You cannot follow yourself."},
                            status=status.HTTP_400_BAD_REQUEST)

        request.user.following.add(target_user)

        return Response({"detail": f"You are now following {target_user.username}."})


        Notification.objects.create(recipient=target_user,actor=request.user,verb="started following you",target=target_user,)


class UnfollowUserView(generics.GenericAPIView):
    queryset = CustomUser.objects.all()     
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def post(self, request, user_id):
        try:
            target_user = CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return Response({"detail": "User not found."},
                            status=status.HTTP_404_NOT_FOUND)

        if not request.user.following.filter(pk=pk).exists():
            return Response({"detail": "You are not following this user."},
                            status=status.HTTP_400_BAD_REQUEST)

        request.user.following.remove(target_user)

        return Response({"detail": f"You have unfollowed {target_user.username}."})
