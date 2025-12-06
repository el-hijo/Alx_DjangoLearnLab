# blog/urls.py

from django.urls import path
from . import views
from .views import (
    CustomLoginView, CustomLogoutView,
    PostListView, PostDetailView,
    PostCreateView, PostUpdateView,
    PostDeleteView,
    CommentCreateView, CommentUpdateView, CommentDeleteView,
    TaggedPostListView,  
    SearchView            
)

app_name = "blog"

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("register/", views.register, name="register"),
    path("profile/", views.profile, name="profile"),

    # Posts
    path("", PostListView.as_view(), name="post-list"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("post/new/", PostCreateView.as_view(), name="post-create"),
    path("post/<int:pk>/update/", PostUpdateView.as_view(), name="post-update"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="post-delete"),

    # Comments
    path("post/<int:pk>/comments/new/", CommentCreateView.as_view(), name="comment-create"),
    path("comment/<int:pk>/update/", CommentUpdateView.as_view(), name="comment-update"),
    path("comment/<int:pk>/delete/", CommentDeleteView.as_view(), name="comment-delete"),


    path("tags/<str:tag_name>/", TaggedPostListView.as_view(), name="posts-by-tag"),

    # NEW — Search URL (even though PostListView handles search)
    path("search/", SearchView.as_view(), name="search"),
]
