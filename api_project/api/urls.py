from django.contrib import admin
from django.urls import path, include
from .views import BookListViewSet, BookList
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'books_all', BookListViewSet, basename='book_all')

urlpatterns = [
    path('books/', BookList.as_view(), name="book-list"),
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
]