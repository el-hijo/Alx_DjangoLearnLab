from django.shortcuts import render
from .models import Book

# Create your views here.
def list_books(request):
    """Retrieves all books and renders a tempate displaying the list."""
    books = Book.objects.all()
    context = {'list_books': books}
    return render(request, 'relationship_app/list_books.html', context)