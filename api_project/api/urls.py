from django.contrib import admin
from django.urls import path
from .views import BookListCreateAPIView


urlpatterns = [
    path('books/', BookList.as_view(), name="book-list"),
    path('admin/', admin.site.urls),
]