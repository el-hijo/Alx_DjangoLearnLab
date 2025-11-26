from django.urls import path
from views import (
    BookListView,
    BookDetailView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView,
)


urlpatterns = [
    # ListView - GET /api/books/
    path("books/", BookListView.as_view(), name="book-list"),

    # DetailView - GET /api/books/<int:pk>/
    path("books/<int:pk>/", BookDetailView.as_view(), name="book-detail"),

    # CreateView - POST /api/books/create/
    path("books/create/", BookCreateView.as_view(), name="book-create"),

    # UpdateView - PUT/PATCH /api/books/<int:pk>/update/
    path("books/<int:pk>/update/", BookUpdateView.as_view(), name="book-update"),

    # DeleteView - DELETE /api/books/<int:pk>/delete/
    path("books/<int:pk>/delete/", BookDeleteView.as_view(), name="book-delete"),
]