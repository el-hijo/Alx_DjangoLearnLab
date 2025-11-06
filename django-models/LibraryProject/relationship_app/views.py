from django.shortcuts import render
from django.views.generic.detail import DetailView
from .models import Book
from .models import Library

# Create your views here.
def list_books(request):
    """Retrieves all books and renders a tempate displaying the list."""
    books = Book.objects.all()
    context = {'list_books': books}
    return render(request, 'relationship_app/list_books.html', context)

class BookDetailView(DetailView):
    """A call_based view for displaying details of a specific library. """
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
    
    def get_context_data(self, **kwargs):
        """Injects additional context data specific to the book."""
        context = super().get_context_data(**kwargs)
        context['book'] = self.object.books.all()
        return context
    
    