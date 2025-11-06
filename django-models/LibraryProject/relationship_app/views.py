from django.http import HttpResponse
from .models import Book

# Create your views here.
def book_list(request):
    """Retrieves all books and renders a tempate displaying the list."""
    books = Book.objects.all()
    output = "List of Books:\n"
    for book in books:
        output += f"-{book.title} by {book.author}"
        
    return HttpResponse(output, content_type= "text/plain")