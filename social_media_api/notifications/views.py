
from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer

# Create your views here.
class NotificationListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NotificationSerializer

    def get_queryset(self):
        # Show unread first, then read
        return Notification.objects.filter(
            recipient=self.request.user
        ).order_by("-unread", "-timestamp")
