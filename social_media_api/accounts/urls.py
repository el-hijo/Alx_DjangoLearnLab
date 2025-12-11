from django.urls import path
from .views import RegisterView, LoginView, FollowUserView, UnfollowUserView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("users/<int:pk>/follow/", FollowUserView.as_view(), name="follow-user"),
    path("users/<int:pk>/unfollow/", UnfollowUserView.as_view(), name="unfollow-user"),
]
